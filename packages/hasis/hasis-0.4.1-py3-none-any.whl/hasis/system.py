
__all__ = (
  'ALPINE',
  'ALPINE_LIKE',
  'ARCH',
  'BUSYBOX',
  'CENTOS',
  'CLT',
  'COMPLETION',
  'CONTAINER',
  'DEBIAN',
  'DEBIAN_FRONTEND',
  'DEBIAN_LIKE',
  'DIST_CODENAME',
  'DIST_ID',
  'DIST_ID_LIKE',
  'DIST_UNKNOWN',
  'DIST_VERSION',
  'FEDORA',
  'FEDORA_LIKE',
  'HOMEBREW_CASK',
  'HOMEBREW_CELLAR',
  'HOMEBREW_ETC',
  'HOMEBREW_KEGS',
  'HOMEBREW_LIB',
  'HOMEBREW_OPT',
  'HOMEBREW_PREFIX',
  'HOMEBREW_PROFILE',
  'HOMEBREW_REPOSITORY',
  'HOMEBREW_TAPS',
  'HOST',
  'HOST_PROMPT',
  'KALI',
  'LINUX',
  'MACOS',
  'NIXOS',
  'PM',
  'PM_INSTALL',
  'RHEL',
  'RHEL_LIKE',
  'SSH',
  'UBUNTU',
  'UNAME',
)

import os
import pathlib

_path = lambda x: _rv if (_rv := os.getenv(x)) is None else pathlib.Path(_rv)

"""'DIST_ID' is 'alpine' and not: nix or busybox"""
ALPINE: bool = bool(os.getenv('ALPINE'))
"""'DIST_ID' is 'alpine'"""
ALPINE_LIKE: bool = bool(os.getenv('ALPINE_LIKE'))
"""'DIST_ID' is 'arch' for archlinux"""
ARCH: bool = bool(os.getenv('ARCH'))
"""if not '/etc/os-release' and not '/sbin'."""
BUSYBOX: bool = bool(os.getenv('BUSYBOX'))
"""'DIST_ID' is 'centos'"""
CENTOS: bool = bool(os.getenv('CENTOS'))
"""Command Line Tools /usr directory (xcode-select -p)"""
CLT: pathlib.Path = _path('CLT')
"""BASH completion instalation path"""
COMPLETION: pathlib.Path = _path('COMPLETION')
"""Running in docker container"""
CONTAINER: bool = bool(os.getenv('CONTAINER')) 
"""'DIST_ID' is 'debian'"""
DEBIAN: bool = bool(os.getenv('DEBIAN'))
"""'noninteractive' if 'IS_CONTAINER' and 'DEBIAN_LIKE' are set"""
DEBIAN_FRONTEND: str = os.getenv('DEBIAN_FRONTEND')
"""'DIST_ID_LIKE is 'debian'"""
DEBIAN_LIKE: bool = bool(os.getenv('DEBIAN_LIKE'))
"""Distribution Codename: Catalina, Big Sur, kali-rolling, focal, etc."""
DIST_CODENAME: str = os.getenv('DIST_CODENAME')
"""alpine|centos|debian|kali|macOS|ubuntu|..."""
DIST_ID: str = os.getenv('DIST_ID')
"""One of: alpine|debian|rhel fedora"""
DIST_ID_LIKE: str = os.getenv('DIST_ID_LIKE')
"""'DIST_ID' is unknown"""
DIST_UNKNOWN: bool = bool(os.getenv('DIST_UNKNOWN'))
"""Distribution Version: macOS (10.15.1, 10.16, ...), kali (2021.2, ...), ubuntu (20.04, ...)"""
DIST_VERSION: str = os.getenv('DIST_VERSION')
"""'DIST_ID' is 'fedora'"""
FEDORA: bool = bool(os.getenv('FEDORA'))
"""'DIST_ID' is 'fedora' or 'fedora' in 'DIST_ID_LIKE'"""
FEDORA_LIKE: bool = bool(os.getenv('FEDORA_LIKE'))
"""Cask Versions (similar to opt)"""
HOMEBREW_CASK: pathlib.Path = _path('HOMEBREW_CASK')
"""Version of formula, $HOMEBREW_PREFIX/opt is a symlink to $HOMEBREW_CELLAR"""
HOMEBREW_CELLAR: pathlib.Path = _path('HOMEBREW_CELLAR')
"""Homebrew etc"""
HOMEBREW_ETC: pathlib.Path = _path('HOMEBREW_ETC')
"""Homebrew unlinked Kegs (in $HOMEBREW_OPT) to add to PATH"""
HOMEBREW_KEGS: pathlib.Path = _path('HOMEBREW_KEGS')
"""Homebrew $HOMEBREW_PREFIX/lib"""
HOMEBREW_LIB: pathlib.Path = _path('HOMEBREW_LIB')
"""Symlink for the latest version of formula to $HOMEBREW_CELLAR"""
HOMEBREW_OPT: pathlib.Path = _path('HOMEBREW_OPT')
"""Homebrew prefix (brew shellenv)"""
HOMEBREW_PREFIX: pathlib.Path = _path('HOMEBREW_PREFIX')
"""Profile compat dir (profile.d), under etc"""
HOMEBREW_PROFILE: pathlib.Path = _path('HOMEBREW_PROFILE')
"""Repository and Library with homebrew gems and Taps (brew shellenv)"""
HOMEBREW_REPOSITORY: pathlib.Path = _path('HOMEBREW_REPOSITORY')
"""Taps path under '$HOMEBREW_REPOSITORY/Library'"""
HOMEBREW_TAPS: pathlib.Path = _path('HOMEBREW_TAPS')
"""First part of hostname: foo.com (foo), example.foo.com (example)"""
HOST: str = os.getenv('HOST')
"""Symbol and 'HOST' if 'CONTAINER' or 'SSH'"""
HOST_PROMPT: str = os.getenv('HOST_PROMPT')
"""'DIST_ID' is 'kali'"""
KALI: bool = bool(os.getenv('KALI'))
"""Is Linux? $UNAME is 'linux'"""
LINUX: bool = os.getenv('LINUX') == 'true'
"""Is macOS? $UNAME is 'darwin'"""
MACOS: bool = os.getenv('MACOS') == 'true'
"""'DIST_ID' is 'alpine' and '/etc/nix'"""
NIXOS: bool = bool(os.getenv('NIXOS'))
"""Default Package Manager: apk, apt, brew, nix and yum"""
PM: str = os.getenv('PM')
"""Default Package Manager with Install Options (Quiet and no cache for containers)"""
PM_INSTALL: str = os.getenv('PM_INSTALL')
"""'DIST_ID' is 'rhel'"""
RHEL: bool = bool(os.getenv('RHEL'))
"""'DIST_ID' is 'rhel' or 'rhel' in 'DIST_ID_LIKE'"""
RHEL_LIKE: bool = bool(os.getenv('RHEL_LIKE'))
"""'SSH_CLIENT' or 'SSH_TTY' or 'SSH_CONNECTION'"""
SSH: bool = bool(os.getenv('SSH'))
"""'DIST_ID' is 'ubuntu'"""
UBUNTU: bool = bool(os.getenv('UBUNTU'))
"""Operating System System Name: darwin or linux (same as 'sys.platform')"""
UNAME: str = os.getenv('UNAME')

