# Copyright (C) 2021 Flowdas Inc. & Dong-gweon Oh <prospero@flowdas.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import asyncio
import inspect
import json

import falcon
from typeable.typing import (
    Any,
    Dict,
    List,
    Literal,
    Union,
    get_type_hints,
)
from typeable import cast, Object, field, Context, dumps, JsonSchema

from . import _errors as errors
from ._http import HttpEndPoint
from ._injector import Injector
from ._main import Main, version
from . import _openrpc


class JsonRpcRequest(Object):
    jsonrpc: Literal['2.0']
    method: str = field(required=True)
    params: Union[Dict[str, Any], list] = field(default_factory=dict)
    id: Union[int, str, None]


class DefaultJsonRpcRoot:
    pass


_FIELD = '_jsonrpc'
_UNPACK = '_jsonrpc_unpack'


class JsonRpcEndPoint(HttpEndPoint, kind='jsonrpc'):
    _root = None
    _dispatch_map = None

    root_class: type = DefaultJsonRpcRoot
    uri_template: str = '/'
    services: Dict[str, type] = {}

    @property
    def root(self):
        if self._root is None:
            self._root = self.root_class()
            for name, cls in self.services.items():  # pragma: no cover
                setattr(self._root, name, cls())
            self._root.rpc = Rpc()
        return self._root

    async def on_get(self, req, resp):
        url = req.forwarded_uri
        raise falcon.HTTPFound('https://playground.open-rpc.org/?url=' + url)

    async def on_post(self, req, resp):
        try:
            if req.content_type and req.content_type not in {'application/json', 'application/json-rpc',
                                                             'application/jsonrequest'}:
                raise errors.HTTPUnsupportedMediaType()
            if not req.content_length:  # pragma: no cover
                raise errors.HTTPLengthRequired()
            if req.content_length > 1048576:  # 1MiB limit
                raise errors.HTTPPayloadTooLarge()

            try:
                data = await req.stream.read()
                data = json.loads(data.decode())
            except Exception as e:
                raise errors.JSONRPCParseError(str(e)) from e

            injector = JsonRpcInjector()
            injector.insert(JsonRpcEndPoint, self)

            if isinstance(data, dict):
                # single
                resp.status, resp.text = await self._dispatch(injector, data)
            elif isinstance(data, list) and data:
                # batch
                # TODO: concurrency
                results = []
                for el in data:
                    try:
                        status, text = await self._dispatch(injector, el)
                        if text:
                            results.append(text)
                    except errors.JSONRPCInvalidRequestError as e:
                        status, text = self._make_error_response(e, None)
                        results.append(text)
                if results:
                    resp.status = falcon.HTTP_OK
                    resp.text = '[' + '\n,'.join(results) + ']'
                else:
                    resp.status, resp.text = falcon.HTTP_ACCEPTED, ''
            else:
                raise errors.JSONRPCInvalidRequestError(())
        except Exception as e:
            resp.status, resp.text = self._make_error_response(e, None)

    async def _dispatch(self, injector, data):
        ctx = Context()
        try:
            with ctx.capture() as err:
                request = cast(JsonRpcRequest, data, ctx=ctx)
        except Exception as e:
            raise errors.JSONRPCInvalidRequestError(err.location) from e
        # check notification
        has_id = hasattr(request, 'id')
        if not has_id:
            request.id = None
        try:
            dm = self._build_dispatch_map()
            method = dm.get(request.method)
            if not method:
                raise errors.JSONRPCMethodNotFoundError()
            try:
                with ctx.capture() as err:
                    args, kwargs = getattr(method, _UNPACK)(
                        request.params, ctx)
                    awaitable = injector.dispatch(method, *args, **kwargs)
            except Exception as e:
                raise errors.JSONRPCInvalidParamsError(err.location) from e
            if has_id:
                result = await awaitable
                return falcon.HTTP_OK, dumps({
                    'jsonrpc': '2.0',
                    'result': result,
                    'id': request.id,
                })
            else:
                asyncio.create_task(awaitable)
                return falcon.HTTP_ACCEPTED, ''
        except Exception as e:
            return self._make_error_response(e, request.id)

    def _make_error_response(self, e, id):
        if isinstance(e, falcon.HTTPError):
            error = {
                'code': e.code,
                'message': e.title,
            }
            if e.description is not None:
                error['data'] = e.description
            status = e.status
        else:
            Main.capture_exception()
            error = {
                'code': -32603,
                'message': 'Internal error',
                'data': str(e),
            }
            status = falcon.HTTP_INTERNAL_SERVER_ERROR
        return status, json.dumps({
            'jsonrpc': '2.0',
            'error': error,
            'id': id,
        }, ensure_ascii=False, separators=(',', ':'))

    def _build_dispatch_map(self):
        if self._dispatch_map is not None:
            return self._dispatch_map
        self._dispatch_map = dm = {}
        memo = {self}

        def walk(instance, prefix):
            memo.add(instance)
            for key, val in inspect.getmembers(instance, inspect.ismethod):
                if isinstance(getattr(val, _FIELD, None), _openrpc.Method):
                    dm[f'{prefix}{key}'] = cast.function(val, keep_async=False)

            for key, val in getattr(instance, '__dict__', {}).items():
                if val in memo:
                    continue
                walk(val, f'{prefix}{key}.')

        walk(self.root, '')
        return dm


class JsonRpcInjector(Injector):
    pass


JsonRpcInjector.register(JsonRpcEndPoint)(None)


def jsonrpc(_=None):
    def deco(func):
        if not inspect.iscoroutinefunction(func):
            raise TypeError
        sig = JsonRpcInjector.instrument(func).signature
        hints = get_type_hints(func)
        params = []
        it = iter(sig.parameters.items())
        next(it)  # remove self
        var_pos_arg = None
        sig_args = []
        Parameter = inspect.Parameter
        for key, val in it:
            param = _openrpc.ContentDescriptor()
            param.name = key
            tp = hints.get(key, Any)
            if val.default == val.empty:
                param.required = True
            if val.kind == val.VAR_POSITIONAL:
                tp = List[tp]
                var_pos_arg = key
            elif val.kind == val.VAR_KEYWORD:
                tp = Dict[str, tp]
            param.schema = JsonSchema(tp)
            params.append(param)
            sig_args.append((key, val.kind, val.default))
        result = _openrpc.ContentDescriptor()
        tp = hints.get('return', Any)
        result.name = 'return'
        result.schema = JsonSchema(tp)
        m = _openrpc.Method()
        m.params = params
        m.result = result

        def unpack(params, ctx):
            if isinstance(params, dict):
                args, kwargs = [], params
                has_var_pos = bool(kwargs.get(var_pos_arg))
                for key, kind, default in sig_args:
                    with ctx.traverse(key):
                        if kind == Parameter.POSITIONAL_ONLY or kind == Parameter.POSITIONAL_OR_KEYWORD:
                            if kind == Parameter.POSITIONAL_OR_KEYWORD and not has_var_pos:
                                break
                            if key in kwargs:
                                args.append(kwargs.pop(key))
                            elif default != Parameter.empty:
                                args.append(default)
                            else:
                                raise TypeError(
                                    f"{m.name}() missing required positional argument: '{key}'")
                        elif kind == Parameter.VAR_POSITIONAL:
                            args.extend(kwargs.pop(key, []))
                        elif kind == Parameter.VAR_KEYWORD:
                            arg = kwargs.pop(key, None)
                            if arg is not None:
                                conflicts = list(kwargs.keys() & arg.keys())
                                if conflicts:
                                    with ctx.traverse(conflicts[0]):
                                        raise TypeError(
                                            f"{m.name}() got multiple values for argument '{conflicts[0]}'")
                                kwargs.update(arg)
                return args, kwargs
            else:
                # should be list
                args, kwargs = [], {}
                kwd_start = None
                if len(params) > len(sig_args):
                    raise TypeError(
                        f"{m.name}() takes {len(sig_args)} arguments but {len(params)} were given")
                for i, arg in enumerate(params):
                    key, kind, default = sig_args[i]
                    if kind == Parameter.POSITIONAL_ONLY or kind == Parameter.POSITIONAL_OR_KEYWORD:
                        args.append(arg)
                    elif kind == Parameter.VAR_POSITIONAL:
                        args.extend(arg)
                        kwd_start = i + 1
                        break
                    else:
                        kwd_start = i
                        break
                if kwd_start is not None:
                    for i in range(kwd_start, len(params)):
                        key, kind, default = sig_args[i]
                        if kind == Parameter.KEYWORD_ONLY:
                            kwargs[key] = params[i]
                        else:  # VAR_KEYWORD
                            arg = params[i]
                            conflicts = list(kwargs.keys() & arg.keys())
                            if conflicts:
                                with ctx.traverse(conflicts[0]):
                                    raise TypeError(
                                        f"{m.name}() got multiple values for argument '{conflicts[0]}'")
                            kwargs.update(arg)
                return args, kwargs

        setattr(func, _FIELD, m)
        setattr(func, _UNPACK, unpack)
        return func

    return deco if _ is None else deco(_)


class Rpc:
    _schema = None

    @jsonrpc
    async def discover(self, endpoint: JsonRpcEndPoint) -> _openrpc.Document:
        if self._schema is None:
            info = _openrpc.Info()
            info.title = 'Flowdas'
            info.version = version
            methods = []
            dm = endpoint._build_dispatch_map()
            for key, val in dm.items():
                method = getattr(val, _FIELD)
                method.name = key
                methods.append(method)
            doc = _openrpc.Document()
            doc.openrpc = '1.2.6'
            doc.info = info
            doc.methods = methods
            self._schema = doc
        return self._schema
