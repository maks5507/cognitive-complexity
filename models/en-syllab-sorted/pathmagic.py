#
# Created by maks5507 (me@maksimeremeev.com)
#

import sys
from pathlib import Path

parent_dirs = Path(__file__).absolute().parents


def add_to_path(num_of_parent_dirs):
    for i in range(1, num_of_parent_dirs + 1):
        sys.path.insert(0, str(parent_dirs[i]))
