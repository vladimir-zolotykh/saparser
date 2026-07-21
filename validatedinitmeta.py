#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Any, get_args, get_origin, get_type_hints, Union
import inspect


def check_type(value: Any, hint: Any) -> bool:
    origin = get_origin(hint)
    if origin is Union:
        return any(check_type(value, h) for h in get_args(hint))
    if hint is Any:
        return True
    return isinstance(value, hint)


class ValidatedInitMeta(type):
    @staticmethod
    def inject_assert(super_init):
        sig = inspect.signature(super_init)
        hints = get_type_hints(super_init)

        def init(*args, **kwargs):
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            for name, value in bound.arguments.items():
                if name not in hints:
                    continue
                hint = hints[name]
                assert check_type(value, hint), (
                    f"{name}={value!r} "
                    f"is {type(value).__name__}, "
                    f"expected {hint!r}"
                )
            return super_init(*args, **kwargs)

        return init

    def __new__(mcls, name, bases, ns):
        if ns.get("_DO_INIT"):
            ns["__init__"] = mcls.inject_assert(ns["__init__"])
        return super().__new__(mcls, name, bases, ns)
