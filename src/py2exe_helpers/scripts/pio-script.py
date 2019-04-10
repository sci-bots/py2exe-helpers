# -*- coding: utf-8 -*-
import sys
import os

from platformio.__main__ import main
import path_helpers as ph


if __name__ == '__main__':
    prefix = ph.path(sys.prefix)
    os.environ['PYTHONEXEPATH'] = prefix.joinpath('python.exe')
    sys.argv[0] = os.environ['PYTHONEXEPATH']
    sys.executable = os.environ['PYTHONEXEPATH']

    os.environ['PLATFORMIO_HOME_DIR'] = prefix.joinpath('share', 'platformio')
    os.environ['PLATFORMIO_LIB_EXTRA_DIRS'] = prefix.joinpath('share',
                                                              'platformio',
                                                              'include')
    sys.exit(main())
