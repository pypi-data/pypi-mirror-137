# Copyright (C) 2021 Flowdas Inc. & Dong-gweon Oh <prospero@flowdas.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from inspect import (
    Signature,
    Parameter,
    signature,
)

from typeable.typing import get_type_hints


class Functor:
    def __init__(self, wrapper, signature):
        self._wrapper = wrapper
        self.signature = signature

    def __call__(self, injector, *args, **kwargs):
        return self._wrapper(injector, *args, **kwargs)


class Injector:
    _registry = {}
    _functors = {}

    def __init__(self):
        self._instances = {}

    def __init_subclass__(cls, **kwargs):
        cls._registry = {}
        cls._functors = {}

    def _insert(self, interface, impl):
        self._instances[interface] = impl

    def insert(self, interface, impl):
        if interface not in self._registry:
            raise TypeError(f"Unknown interface '{interface.__qualname__}'")
        self._insert(interface, impl)

    @classmethod
    def register(cls, interface):

        def deco(factory):
            if interface in cls._registry:
                raise RuntimeError(f"Ambiguous `{cls.__qualname__}.register()`")
            cls._registry[interface] = None if factory is None else cls.instrument(factory)
            return factory

        return deco

    @classmethod
    def _instrument(cls, func) -> Functor:
        sig = signature(func)
        type_hints = get_type_hints(func)
        depargs = {}
        for name, type in type_hints.items():
            if name == 'return':
                continue
            if type in cls._registry:
                kind = sig.parameters[name].kind
                if kind == Parameter.VAR_POSITIONAL or kind == Parameter.VAR_KEYWORD:
                    raise TypeError(f"Dependency argument cannot be {str(kind)}: '{name}'.")
                depargs[name] = [name, type, None, kind == Parameter.POSITIONAL_ONLY]
        for i, name in enumerate(sig.parameters):
            if name in depargs:
                kind = sig.parameters[name].kind
                if kind != Parameter.KEYWORD_ONLY:
                    depargs[name][2] = i

        deps = tuple(depargs.values())

        def wrapper(injector, *args, **kwargs):
            args = list(args)
            for name, type, idx, posonly in deps:
                if posonly:  # pragma: no cover (>=3.8)
                    if len(args) < idx:
                        raise TypeError
                    args.insert(idx, injector.inject(type))
                elif idx is None:
                    kwargs[name] = injector.inject(type)
                elif len(args) > idx:
                    args.insert(idx, injector.inject(type))
                else:
                    kwargs[name] = injector.inject(type)
            return func(*args, **kwargs)

        if len(deps) == 0:
            s = sig
        else:
            params = [v for k, v in sig.parameters.items() if k not in depargs]
            s = Signature(params, return_annotation=sig.return_annotation)
        cls._functors[func] = functor = Functor(wrapper, s)
        return functor

    @classmethod
    def instrument(cls, func) -> Functor:
        if isinstance(func, Functor):
            return func
        if func in cls._functors:
            return cls._functors[func]
        return cls._instrument(func)

    def inject(self, interface):
        impl = self._instances.get(interface)
        if impl is None:
            factory = self._registry[interface]
            if factory is None:
                raise TypeError(f"Interface '{interface.__qualname__}' not available")
            self._instances[interface] = impl = factory(self)
        return impl

    def dispatch(self, func, *args, **kwargs):
        if not isinstance(func, Functor):
            func = self.instrument(func)
        return func(self, *args, **kwargs)
