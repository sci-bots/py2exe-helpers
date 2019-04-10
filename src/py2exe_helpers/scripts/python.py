'''
Incomplete Python emulator.

Support for:

 - Running a Python script file
 - Running a Python module with ``-m`` flag

Does not support any other ``python.exe`` options or flags, e.g., ``-b``,
``-Q`` (see ``python.exe -h`` for all flags supported by actual CPython).
'''
import sys
import path_helpers as ph
import runpy


if __name__ == "__main__":
    import multiprocessing

    multiprocessing.freeze_support()

    if '-h' in sys.argv:
        print >> sys.stderr, "Usage: python {-m <module> | <script filepath>} [arg [arg ...]]"
        sys.exit(-1)
    elif len(sys.argv) < 2:
        # No script or module was specified. Emulate console using IPython.
        import IPython
        IPython.embed()
        sys.exit()
    elif sys.argv[1] == '-m':
        # Emulate `python -m <module>`.
        del sys.argv[:2] # Make the requested module sys.argv[0]
        runpy._run_module_as_main(sys.argv[0])
    else:
        __filepath__ = ph.path(sys.argv[1]).realpath()
        __file__ = str(__filepath__)
        sys.path.insert(0, __filepath__.parent)
        exec(__filepath__.text())
