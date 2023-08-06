# Copyright (C) 2021 Flowdas Inc. & Dong-gweon Oh <prospero@flowdas.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import asyncio
import getopt
import inspect
import json
import pprint
import sys
import traceback

from typeable import cast, JsonValue

from ._config import Config, EndPoint
from ._injector import Injector
from ._main import Main
from ._jsonrpc import JsonRpcEndPoint

_COMMAND = '__COMMAND'


class _Command:
    __slots__ = (
        'function',
    )

    def __init__(self, *, function):
        self.function = function


def command(_=None):
    def deco(func):
        setattr(func, _COMMAND, _Command(
            function=None,
        ))
        return func

    return deco if _ is None else deco(_)


class _Group:
    __slots__ = ('_getter', '_name')

    def __init__(self, getter):
        self._getter = getter

    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = self._getter(instance)
        setattr(instance, self._name, value)
        return value

    def __set_name__(self, owner, name):
        self._name = name


def group(_=None):
    def deco(func):
        return _Group(func)

    return deco if _ is None else deco(_)


class DefaultConsoleRoot:
    @group
    def rpc(self):
        for ep in Main.config.endpoints:
            if ep.type == 'jsonrpc':
                dm = ep._build_dispatch_map()
                break
        else:  # pragma: no cover
            dm = {}
        attrs = {}
        for k, v in dm.items():
            def wrapper(self, a: int):  # pragma: no cover
                pass

            wrapper.__name__ = k
            setattr(wrapper, _COMMAND, _Command(
                function=v,
            ))
            attrs[k] = wrapper
            Rpc = type('Rpc', (), attrs)
            this = Rpc()
        return this

    @command
    def config(self):
        return Main.config

    @command
    def run(self):
        from typeable import cast, JsonValue
        import uvicorn
        from ._http import HttpEndPoint

        app = None
        for endpoint in Main.config.endpoints:
            if isinstance(endpoint, HttpEndPoint):
                app = endpoint.get_app()
                break
        if app:
            if Main.config.sentry:  # pragma: no cover
                from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
                app = SentryAsgiMiddleware(app)
            opts = cast(JsonValue, Main.config.uvicorn)
            uvicorn.run(app, **opts)

    @command
    def version(self):
        from ._main import version
        print(version)


class ConsoleEndPoint(EndPoint, kind='console'):
    _root = None

    root_class: type = DefaultConsoleRoot

    @property
    def root(self):
        if self._root is None:
            self._root = self.root_class()
        return self._root

    def _parse_args(self, _args):
        args = []
        kwargs = {}
        for arg in _args:
            idx = arg.find('=')
            if idx >= 0:
                key = arg[:idx]
                if key.isidentifier():
                    val = arg[idx + 1:]
                    try:
                        val = json.loads(val)
                    except:
                        pass
                    kwargs[key] = val
                    continue
            if kwargs:
                raise SyntaxError("positional argument follows keyword argument")
            try:
                val = json.loads(arg)
            except:
                val = arg
            args.append(val)
        return args, kwargs

    def dispatch(self, injector, node, args, opts):
        if not args:
            return self.help_group(node)
        name = args[0]
        if isinstance(getattr(node.__class__, name, None), _Group):
            # group
            return self.dispatch(injector, getattr(node, name), args[1:], opts)
        attr = getattr(node, name, None)
        if attr is None:
            return self._error(name)
        if inspect.ismethod(attr):
            cmd = getattr(attr, _COMMAND, None)
            if cmd is None:
                return self._error(name)
            args, kwargs = self._parse_args(args[1:])
            if 'h' in opts:
                return self.help_command(attr, cmd, args, kwargs)
            else:
                if cmd.function is None:
                    cmd.function = cast.function(attr, keep_async=False)
                return injector.dispatch(cmd.function, *args, **kwargs)
        return self._error(name)

    def _print_command_help(self, method, cmd):
        if cmd.function:
            functor = ConsoleInjector.instrument(cmd.function)
        else:
            functor = ConsoleInjector.instrument(method)
        print(f"{method.__name__}{functor.signature}")

    def help_command(self, method, cmd, args, kwargs):
        self._print_command_help(method, cmd)
        sys.exit(2)

    def help_group(self, node):
        print('Commands:\n')
        methods = inspect.getmembers(node, inspect.ismethod)
        for name, method in sorted(methods):
            cmd = getattr(method, _COMMAND, None)
            if cmd is not None:
                self._print_command_help(method, cmd)

        groups = [k for k, v in inspect.getmembers(node.__class__) if isinstance(v, _Group)]
        if groups:
            print('\nGroups:\n')
            for g in groups:
                print(g)
        sys.exit(2)

    def _error(self, name):
        print(f"'{name}' is not a command.")
        sys.exit(2)

    def main(self, args=None):
        if args is None:  # pragma: no cover
            args = sys.argv[1:]
        try:
            optlist, args = getopt.getopt(args, 'dh')
        except getopt.GetoptError:
            return self.help_group(self.root)
        opts = ''.join(sorted(opt[1:] for opt, _ in optlist))
        if 'd' in opts:
            Main.config.debug = True
        injector = ConsoleInjector()
        injector.insert(ConsoleEndPoint, self)
        for ep in Main.config.endpoints:
            if ep.type == 'jsonrpc':
                injector.insert(JsonRpcEndPoint, ep)
                break
        try:
            result = self.dispatch(injector, self.root, args, opts)
            if inspect.isawaitable(result):
                result = asyncio.get_event_loop().run_until_complete(result)
            if result is not None:
                pprint.pprint(cast(JsonValue, result))
        except Exception as e:
            if Main.config.sentry:  # pragma: no cover
                Main.capture_exception()
            if Main.config.debug:
                traceback.print_exc()
            else:
                print(f"{e.__class__.__name__}: {e}")
            return 1
        return 0


class ConsoleInjector(Injector):
    pass


ConsoleInjector.register(ConsoleEndPoint)(None)
ConsoleInjector.register(JsonRpcEndPoint)(None)
