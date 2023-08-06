# Copyright 2021 Cognite AS
from collections import defaultdict
from distutils.version import StrictVersion
from typing import Any, Callable, DefaultDict, Dict, List, Optional, Sequence

from .type_check import check_types


_registered_funcs: DefaultDict[str, Dict[str, Any]] = defaultdict(dict)


@check_types
def register(
    version: str,
    name: Optional[str] = None,
    deprecated: Optional[bool] = False,
    deprecation_warning: Optional[str] = None,
):
    """Decorator to register a new versioned function.

    Args:
        version (str): Version number of the function
            The version number follows the distutils strict version standard.

            The following are valid version numbers (shown in the order that
            would be obtained by sorting according to the supplied cmp function):

                0.4       0.4.0  (these two are equivalent)
                0.4.1
                0.5a1
                0.5b3
                0.5
                0.9.6
                1.0
                1.0.4a3
                1.0.4b1
                1.0.4

            The following are examples of invalid version numbers:

                1
                2.7.2.2
                1.3.a4
                1.3pl1
                1.3c4
        name (str, optional): Name of the function
            The name under which the function should be registered. If no name
            is specified, the name of the funtion is used.
        deprecated (bool, optional): Flag is function is deprecated. Default: False
        deprecation_warning (str, optional): Deprecation warning message. Default: None
    """

    # Test that the version numbering is valid
    StrictVersion(version)

    def register_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """ Register a new versioned function """

        key = name or func.__name__

        if version in _registered_funcs[key]:
            raise ValueError(f"Function {key} with version {version} is already registered")

        _registered_funcs[key][version] = func

        func.__versioning_version__ = version  # type: ignore
        func.__versioning_name__ = key  # type: ignore
        func.__versioning_deprecated__ = deprecated  # type: ignore
        func.__versioning_deprecation_warning__ = deprecation_warning  # type: ignore

        return func

    return register_decorator


def get_registered_functions() -> List[str]:
    """ Return the list of registered function names """

    return list(_registered_funcs.keys())


@check_types
def get_versions(name: str) -> List[str]:
    """Return the list of available versions of a function name.
    Sorted from low to highest version"""

    versions = _registered_funcs[name].keys()
    return sorted(versions, key=StrictVersion)


@check_types
def get_name(func: Callable[..., Any]) -> str:
    """Return the name with which the function was registered"""

    try:
        return func.__versioning_name__  # type: ignore
    except AttributeError:
        raise ValueError("Cannot get name of an un-registerd function")


@check_types
def get_version(func: Callable[..., Any]) -> Optional[str]:
    """Return the version of a function. If the function is not registered, None is returned """

    try:
        return func.__versioning_version__  # type: ignore
    except AttributeError:
        return None


@check_types
def is_versioned(func: Callable[..., Any]) -> bool:
    """Return true if the version is versioned """

    return hasattr(func, "__versioning_version__")


@check_types
def is_deprecated(func: Callable[..., Any]) -> Optional[bool]:
    """Return true if the version is deprecated. If the function is not registered, None is returned """

    try:
        return func.__versioning_deprecated__  # type: ignore
    except AttributeError:
        return None


@check_types
def get_deprecation_warning(func: Callable[..., Any]) -> Optional[str]:
    """Return depreaction warning of the version. If the function is not registered, None is returned """

    try:
        return func.__versioning_deprecation_warning__  # type: ignore
    except AttributeError:
        return None


@check_types
def get(name: str, version: Optional[str] = None) -> Callable[..., Any]:
    """Return one of the versions of a function.
    If version is None, the latest version is returned"""

    if version is None:
        version = get_versions(name)[-1]

    if name not in _registered_funcs:
        raise ValueError(f"Function {name} is not registered")
    if version not in _registered_funcs[name]:
        raise ValueError(f"Version {version} for function {name} is not registered")
    return _registered_funcs[name][version]


@check_types
def run(
    name: str, version: Optional[str] = None, args: Optional[Sequence] = None, kwargs: Optional[dict] = None
) -> Any:
    """Run a version of a function.
    If version is None, the latest version is executed"""

    if args is None:
        args = []
    if kwargs is None:
        kwargs = {}
    return get(name, version)(*args, **kwargs)
