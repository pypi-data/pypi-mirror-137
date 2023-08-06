from __future__ import annotations

import os
from shutil import copy2
from shutil import make_archive
from typing import Tuple, Iterable


def get_labeled_files(path: str) -> list:
    labeled_files = []

    for root, _, filenames in os.walk(path, topdown=True):
        filenames.sort()
        for index, filename in enumerate(filenames):
            if filename.endswith(".xml"):
                img = os.path.join(root, filenames[index - 1])
                xml = os.path.join(root, filename)
                labeled_files.append((img, xml))

    return labeled_files


def _copy(sources: Iterable[Tuple[str]], dst: str):
    for src1, src2 in sources:
        copy2(src1, dst)
        copy2(src2, dst)


def archive(dest_dir: str, src, _format: str = 'zip'):
    make_archive(dest_dir, _format, src)
