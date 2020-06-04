#
# Created by maks5507 (me@maksimeremeev.com)
#

import os

def create_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
