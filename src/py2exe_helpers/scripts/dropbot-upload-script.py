# -*- coding: utf-8 -*-
if __name__ == '__main__':
    import os
    import sys
    import subprocess as sp

    import path_helpers as ph

    prefix = ph.path(sys.prefix)
    os.environ['PYTHONEXEPATH'] = prefix.joinpath('python.exe')
    sys.argv[0] = os.environ['PYTHONEXEPATH']
    sys.executable = os.environ['PYTHONEXEPATH']

    p = sp.Popen([prefix.joinpath('Scripts', 'wrappers', 'conda',
                                  'run-in.bat'), sys.executable, '-m',
                  'dropbot.bin.upload'])
    sys.exit(p.wait())
