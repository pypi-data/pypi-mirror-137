from typeguard import typeguard_ignore
from typeguard.importhook import install_import_hook

from boba_fetch.rpc import UnixSocketRPCServer

install_import_hook('boba')

typeguard_ignore(UnixSocketRPCServer.server)
typeguard_ignore(UnixSocketRPCServer.proxy)
