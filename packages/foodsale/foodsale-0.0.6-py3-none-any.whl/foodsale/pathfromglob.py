import os
import pathlib
import re
from typing import List


def abspathglob(*globs: List[str], excludes: List[str] = None) -> List[pathlib.Path]:
    paths = set()

    for _str in globs:
        absolute = pathlib.Path(_str)
        relative = str(absolute).lstrip(absolute.anchor)
        cwd = pathlib.Path.cwd()
        try:
            os.chdir(absolute.anchor)
            glob = pathlib.Path(absolute.anchor).glob(relative)
        finally:
            os.chdir(cwd)

        paths = {path for path in glob}

    if excludes:
        for path in paths.copy():
            for regex in excludes:
                if re.search(regex, str(path), re.IGNORECASE):
                    paths.remove(path)

    return list(paths)


def main():
    pass


if __name__ == "__main__":
    main()
