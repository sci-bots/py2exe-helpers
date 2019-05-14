'''
Static files to copy relative to distribution root.

Helper functions to populate ``data_files`` property of ``py2exe`` setup.
'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import glob
import itertools as it
import os
import re

import path_helpers as ph


__all__ = ['DEFAULT_STATIC_PREFIX', 'get_data_files', 'group_data_files']


DEFAULT_STATIC_PREFIX = {'__core__': {'files': [{'source': '$PY2EXE_HELPERS/scripts/run-in.bat', 'target': 'Scripts/wrappers/conda'},
                                                {'source': 'MSVCP90.dll', 'target': ''},
                                                {'source': '$PY2EXE_HELPERS/scripts/py2exe-python-emulation.bat', 'target': 'etc/conda/activate.d'}]},
                         'microdrop': {'files': [{'source': '$CONDA_PREFIX/etc/conda/', 'target': 'etc/conda'},
                                                 {'source': '$CONDA_PREFIX/etc/microdrop/', 'target': 'etc/microdrop'}]},
                         'nbformat': {'files': [{'source': '$MODULE/', 'target': 'nbformat'}]},
                         'notebook': {'files': [{'source': '$PY2EXE_HELPERS/scripts/jupyter-notebook.py', 'target': 'Scripts'},
                                                {'source': '$MODULE/static/', 'target': 'notebook/static'},
                                                {'source': '$MODULE/templates/', 'target': 'notebook/templates'}]},
                         'numpy': {'files': [{'source': 'libiomp5md.dll', 'target': ''},
                                             {'source': 'mkl_*.dll', 'target': ''}]},
                         'pandoc': {'files': [{'source': '$CONDA_PREFIX/Scripts/pandoc.exe', 'target': 'Scripts'}]},
                         'platformio': {'files': [{'source': '$PY2EXE_HELPERS/scripts/pio.bat', 'target': 'Scripts'},
                                                  {'source': '$MODULE/builder/', 'target': 'platformio/builder'},
                                                  {'source': '$CONDA_PREFIX/share/platformio/', 'target': 'share/platformio'}]},
                         'pygst-0.10': {'module': 'gst', 'files': [{'source': '$MODULE/bin/*.dll', 'target': ''},
                                                                   {'source': '$PY2EXE_HELPERS/scripts/gst-plugins-path.bat', 'target': 'etc/conda/activate.d'},
                                                                   {'source': '$MODULE/plugins/*.dll', 'target': 'gst-plugins'}]},
                         'pygtk2': {'module': 'gtk', 'files': [{'source': '$MODULE/../gtk_runtime/share/themes/MS-Windows/gtk-2.0/', 'target': 'etc/gtk-2.0'},
                                                               {'source': '$MODULE/../gtk_runtime/lib/gtk-2.0/2.10.0/engines/*.dll', 'target': 'lib/gtk-2.0/2.10.0/engines'},
                                                               {'source': '$MODULE/../gtk_runtime/share/icons/hicolor/', 'target': 'share/icons/hicolor'}]},
                         'pyzmq': {'module': 'zmq', 'files': [{'source': '$MODULE/libzmq.pyd', 'target': ''}]},
                        }

try:
    import pymunk
    DEFAULT_STATIC_PREFIX['pymunk'] = {'files': [{'source':
                                                  pymunk.cp.chipmunk_lib._name,
                                                  'target': ''}]}
except ImportError:
    # `pymunk` is not installed in build environment.
    pass


def walk_syspath(name_glob):
    '''Find all files matching specified pattern on executable path.

    Parameters
    ----------
    name_glob : str
        Glob file pattern to match (e.g., accepts ``*`` as wildcard).

    Yields
    ------
    path_helpers.path
        Path to file matching specified pattern found on executable path.
    '''
    for p in [ph.path(p).expand() for p in os.environ['PATH'].split(';')]:
        if p.isdir():
            for f in p.files(name_glob):
                yield f


def find_executables(name_glob):
    '''Return all distinct executables matching specified pattern.

    If multiple executables are found with the same filename, use the first
    path found in order of paths in ``$PATH`` environment variable.

    Parameters
    ----------
    name_glob : str
        Glob file pattern to match (e.g., accepts ``*`` as wildcard).

    Returns
    -------
    list[path_helpers.path]
        List of matching executable paths.
    '''
    all_matching_dlls = list(walk_syspath(name_glob))
    return zip(*sorted({f.name: f for f in reversed(all_matching_dlls)}
                       .items()))[1]


def get_package_prefix_files(package_specs, static_prefix=None):
    static_prefix = static_prefix or DEFAULT_STATIC_PREFIX
    package_specs = package_specs[:]
    package_specs.insert(0, '__core__')

    # Save shell envionment.
    init_env = os.environ.copy()

    try:
        os.environ['PY2EXE_HELPERS'] = ph.path(__file__).parent
        os.environ['SRC'] = os.getcwd()
        static_files = {}
        for package_spec_i in package_specs:
            name_i = re.split(r'=+', package_spec_i)[0]
            if name_i in static_prefix:
                package_config_i = static_prefix[name_i]
                try:
                    os.environ['MODULE'] = __import__(package_config_i
                                                      .get('module',
                                                           name_i)).__path__[0]
                except ImportError:
                    if 'MODULE' in os.environ:
                        del os.environ['MODULE']

                def _package_prefix_files(prefix_files):
                    files = []
                    for f in prefix_files:
                        source_ij = ph.path(f['source']).expand()
                        if '*' in source_ij and glob.glob(source_ij):
                            files.extend(
                                _package_prefix_files([{'source': p,
                                                        'target': f['target']}
                                                       for p in
                                                       glob.glob(source_ij)]))
                            continue
                        elif source_ij.isdir():
                            files.extend([{'source': p, 'target':
                                           ph.path(f['target'])
                                           .joinpath(source_ij
                                                     .relpathto(p.parent))
                                           .normpath()}
                                          for p in source_ij.walkfiles()])
                            continue
                        elif source_ij.isfile():
                            pass
                        elif source_ij.ext.lower() == '.dll':
                            exes_ij = find_executables(source_ij)
                            files.extend(
                                _package_prefix_files([{'source': p,
                                                        'target': f['target']}
                                                       for p in exes_ij]))
                            continue
                        elif not source_ij.isfile():
                            continue
                        files.append({'source': source_ij,
                                      'target': f['target']})
                    return files

                files = _package_prefix_files(package_config_i.get('files',
                                                                   []))
                static_files[name_i] = files
    finally:
        os.environ = init_env
    return static_files


def get_data_files(package_specs, static_prefix=None):
    static_files = get_package_prefix_files(package_specs,
                                            static_prefix=static_prefix)
    return sorted([tuple(map(str, (f['target'], f['source'])))
                   for s in static_files for f in static_files[s]])


def group_data_files(data_files):
    '''Group list of data file tuples by destination.

    Parameters
    ----------
    data_files : list[(str, str)]
        List of ``(<relative dest dir path>, <absolute source file path>)``
        items.

    Returns
    -------
    list[(str, list[str])]
        Input source file paths grouped by relative destination directory.
    '''
    return [(i, [f[1] for f in g]) for i, g in it.groupby(data_files,
                                                          lambda x: x[0])]
