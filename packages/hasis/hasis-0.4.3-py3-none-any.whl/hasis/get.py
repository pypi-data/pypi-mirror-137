
__all__ = (
    'ExcType',
    'suppress',
    'tilde',
    'version',    
)

import importlib.metadata
import contextlib
from pathlib import Path
from collections.abc import Callable
from typing import Any
from typing import Callable
from typing import ParamSpec
from typing import TypeAlias
from typing import TypeVar


T = TypeVar('T')
P = ParamSpec('P')

ExcType: TypeAlias = Exception | tuple[Exception, ...]

def suppress(func: Callable[P, T], exc: ExcType | None = None, *args: P.args, **kwargs: P.kwargs) -> T:
    """Try and supress exception"""
    with contextlib.suppress(exc or Exception): 
        return func(*args, **kwargs)

def tilde(path: str | Path = '.') -> str:
    """Replaces $HOME with ~"""
    return str(path).replace(str(Path.home()), '~')
            
def version(package: str = None) -> str:
    """Package installed version"""
    return suppress(importlib.metadata.version, importlib.metadata.PackageNotFoundError, 
                    package or pathlib.Path(__file__).parent.name)
