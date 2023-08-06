import os
import pathlib
from typing import List


def abspathglob(*sglobs) -> List[pathlib.Path]:
    paths = set()

    for _str in sglobs:
        absolute = pathlib.Path(_str)
        relative = str(absolute).lstrip(absolute.anchor)
        cwd = pathlib.Path.cwd()
        try:
            os.chdir(absolute.anchor)
            glob = pathlib.Path(absolute.anchor).glob(relative)
        finally:
            os.chdir(cwd)

        for path in list(glob):
            paths.add(path)

    return list(paths)


def main():
    pass


if __name__ == "__main__":
    main()
