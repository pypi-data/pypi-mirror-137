
__all__ = (
    'ExcType',
    'suppress',
    'version',    
)

import importlib.metadata
import pathlib
import contextlib
from typing import Any
from typing import Callable
from typing import Optional
from typing import Union

ExcType = Union[Exception, tuple[Exception, ...]]

def tilde(path: Union[str, pathlib.Path] = '.') -> str:
    """Replaces $HOME with ~"""
    return str(path).replace(str(Path.home()), '~')
    
def suppress(func: Callable, exc: Optional[ExcType] = None, *args: Any, **kwargs: Any) -> Any:
    """Try and supress exception"""
    with contextlib.suppress(exc or Exception): 
        return func(*args, **kwargs)
        

def version(package: str = None) -> str:
    """Package installed version"""
    return suppress(importlib.metadata.version, importlib.metadata.PackageNotFoundError, 
                    package or pathlib.Path(__file__).parent.name)
        
 
