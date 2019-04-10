'''
Console script definitions.

Helper functions to populate ``console`` property and ``windows`` property of
``py2exe`` setup.
'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import os
import re
import runpy

import path_helpers as ph


__all__ = ['DEFAULT_CONSOLE_SCRIPTS', 'DEFAULT_WINDOWS_EXES',
           'get_console_scripts', 'get_windows_exes']


runpy_file = os.path.join(os.path.split(runpy.__file__)[0], 'runpy.py')

def strip_script_suffix(f):
    f = ph.path(f)
    return {'script': f, 'dest_base': f.namebase.rstrip('-script')}


DEFAULT_CONSOLE_SCRIPTS = {'__core__': [runpy_file],
                           'dropbot': ['$PY2EXE_HELPERS/scripts/dropbot-upload-script.py'],
                           'ipython': ['$PY2EXE_HELPERS/scripts/python.py'],
                           'jupyter': ['$PY2EXE_HELPERS/scripts/jupyter-notebook.py'],
                           'platformio': ['$PY2EXE_HELPERS/scripts/pio-script.py']}
DEFAULT_WINDOWS_EXES = {}


try:
    import microdrop

    microdrop_icon = ph.path(microdrop.__file__).parent.joinpath('microdrop.ico')

    DEFAULT_CONSOLE_SCRIPTS['microdrop'] = \
        ['$CONDA_PREFIX/Scripts/microdrop-config-script.py',
         # Package alternate MicroDrop executable to launch from console. This
         # may be helpful, for example, during debugging, since `stdout` and
         # `stderr` are written to the output of the console where MicroDrop
         # was launched from.  In contrast, the MicroDrop Windows executable
         # (with the graphical icon) *launches a **new** console*.
         {'script': '$PY2EXE_HELPERS/scripts/microdrop-exe.py',
          'dest_base': 'microdrop-console',
          # XXX Need to include `icon_resources` otherwise icon is also missing
          # from `windows` executable above.  This seems like it must have
          # something to do with the two scripts sharing the same source, where
          # the Windows app manifest does not seem to be written correctly.
          'icon_resources': [(0, microdrop_icon)]}]
    DEFAULT_WINDOWS_EXES['microdrop'] = \
        [# Package MicroDrop executable as a *Windows* application (as opposed to
         # a *console* application).  This is necessary to assign an icon to the
         # `.exe` file.
         {'script': '$PY2EXE_HELPERS/scripts/microdrop-exe.py',
          'dest_base': 'MicroDrop',
          'icon_resources': [(0, microdrop_icon)]}]
except ImportError:
    pass


def get_scripts(package_specs, package_scripts):
    '''Get list of script references.

    Any script name including the suffix ``-script`` will have the suffix
    removed in the resulting executable name..

    Parameters
    ----------
    package_specs : list[str]
        List of Conda package specifiers, e.g., from the dependencies section
        of a Conda environment YAML file.
    static_packages : dict[str->dict]
        Mapping from Conda package name to static package configuration.  Each
        configuration **MAY** include any of the following keys::

         - ``module``: Python module name (if different than the Conda package
           name)
         - ``dirs``: list of directories to scan for static files, relative to
           module path (search all directories if not set)

    Returns
    -------
    list[path_helpers.path or dict]
        List of file paths to static contents of specified packages.
    '''
    package_specs = package_specs[:]
    package_specs.insert(0, '__core__')

    scripts = []

    # Save shell envionment.
    init_env = os.environ.copy()

    try:
        os.environ['PY2EXE_HELPERS'] = ph.path(__file__).parent
        for package_spec_i in package_specs:
            name_i = re.split(r'=+', package_spec_i)[0]
            if name_i in package_scripts:
                for script_ij in package_scripts[name_i]:
                    if isinstance(script_ij, dict):
                        script_path_ij = ph.path(script_ij['script']).expand()
                        script_ij = script_ij.copy()
                        script_ij['script'] = str(script_path_ij)
                    else:
                        script_path_ij = ph.path(script_ij).expand()
                        if script_path_ij.namebase.endswith('-script'):
                            # Script ends with `-script`.  Automatically rename
                            script_ij = {'script': str(script_path_ij),
                                         'dest_base': script_path_ij.namebase
                                         .rstrip('-script')}
                        else:
                            script_ij = str(script_path_ij)
                    scripts.append(script_ij)
    finally:
        os.environ = init_env
    return scripts


def get_console_scripts(package_specs, package_console_scripts=None):
    package_console_scripts = (package_console_scripts or
                               DEFAULT_CONSOLE_SCRIPTS)
    return get_scripts(package_specs, package_scripts=package_console_scripts)


def get_windows_exes(package_specs, package_windows_exes=None):
    package_exes = (package_windows_exes or DEFAULT_WINDOWS_EXES)
    return get_scripts(package_specs, package_scripts=package_exes)
