'''
Static files to include in site-packages or `library.zip`
'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import re
import sys

import path_helpers as ph

__all__ = ['DEFAULT_STATIC_PACKAGES', 'conda_collector']


DEFAULT_STATIC_PACKAGES = {'ipython': {'module': 'IPython', 'dirs': ['core/profile']},
                           'dropbot': {},
                           'jsonschema': {},
                           'microdrop': {},
                           'nbformat': {},
                           'notebook': {},
                           'pint': {},
                           'wheeler.pygtkhelpers': {'module': 'pygtkhelpers'},
                           'teensy-minimal-rpc': {'module': 'teensy_minimal_rpc'}}


def get_package_static_files(package_specs, static_packages=None):
    '''
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
    list[path_helpers.path]
        List of file paths to static contents of specified packages.
    '''
    static_packages = static_packages or DEFAULT_STATIC_PACKAGES
    package_files = []
    for dependency_i in package_specs:
        name_i = re.split(r'=+', dependency_i)[0]
        if name_i in static_packages:
            package_i = static_packages[name_i]
            module_i = __import__(package_i.get('module', name_i))
            module_path_i = ph.path(module_i.__path__[0]).realpath()
            for site_dir_i in map(ph.path, reversed(sys.path)):
                if module_path_i.startswith(site_dir_i):
                    break
            else:
                raise RuntimeError('`%s` not found in any of: %s' %
                                   (module_path_i, sys.path))
            package_files_i = []
            for dir_ij in package_i.get('dirs', ['']):
                package_files_i.extend([{'target': site_dir_i.relpathto(f), 'source': f}
                                        for f in module_path_i.joinpath(dir_ij).walkfiles()
                                        if not f.ext.startswith('.py')])
            package_files.extend(package_files_i)
    return package_files


def conda_collector(*args, **kwargs):
    '''Create custom py2exe setup command class to include default static files
    for specified Conda packages.

    Parameters
    ----------
    *args, **kwargs
        See :func:`get_package_static_files()`.

    Returns
    -------
    distutils.cmd.Command
        Command class for setup.
    '''
    from py2exe.build_exe import py2exe as build_exe

    package_files = get_package_static_files(*args, **kwargs)

    class CondaCollector(build_exe):
        def copy_extensions(self, extensions):
            build_exe.copy_extensions(self, extensions)
            collect_dir = ph.path(self.collect_dir)

            for package_file_i in package_files:
                collected_i = collect_dir.joinpath(package_file_i['target'])
                collected_i.parent.makedirs_p()
                self.copy_file(package_file_i['source'], collected_i)
                self.compiled_files.append(package_file_i['target'])

    return CondaCollector
