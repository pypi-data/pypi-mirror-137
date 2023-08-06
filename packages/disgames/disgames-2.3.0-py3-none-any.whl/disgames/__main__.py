import aiohttp
import argparse
import platform
from __init__ import VersionInfo
from typing import Tuple

def version() -> None:
    entries = []

    entries.append('- Python v{0.major}.{0.minor}.{0.micro}-{0.releaselevel}'.format(sys.version_info))
    version_info: VersionInfo = VersionInfo(major=2, minor=3, micro=0)
    entries.append('- Disgames v{0.major}.{0.minor}.{0.micro}'.format(version_info))
    entries.append(f'- aiohttp v{aiohttp.__version__}') 
    entries.append(f'- Chess v{chess.__version__}')

    uname = platform.uname()
    entries.append('- System Info: {0.system} {0.release} {0.version}'.format(uname))

def show_version(parser, args) -> None:
    if args.version:
        version()


def parse_args() -> Tuple[argparse.ArgumentParser, argparse.Namespace]:
    parser = argparse.ArgumentParser(prog='disgames', description='Tools for helping with disgames')
    parser.add_argument('-v', '--version', action='store_true', help='shows the library version')
    parser.set_defaults(func=show_version)

    return parser, parser.parse_args()

def main() -> None:
    parser, args = parse_args()
    args.func(parser, args)

if __name__ == '__main__':
    main()
