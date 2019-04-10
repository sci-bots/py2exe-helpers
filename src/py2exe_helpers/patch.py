from __future__ import absolute_import, print_function
import re
import site
import subprocess as sp
import sys

import path_helpers as ph


__all__ = ['DEFAULT_TOUCH_INIT', 'apply_patches', 'fix_init']


def apply_patches(patches_dir=None):
    '''
    Apply patches in specified directory.

    First line of each patch file is path to file to be patched, relative to
    the :attr:`sys.prefix` directory.

    Skip patches if they have already been applied.

    Parameters
    ----------
    patches_dir : str, optional
        Directory containing patch files.
    '''
    if patches_dir is None:
        patches_dir = ph.path(__file__).parent.joinpath('patches')
    sys_prefix = ph.path(sys.prefix)
    patches_dir = ph.path(patches_dir).realpath()
    if not patches_dir.isdir():
        return
    for patch_file_i in patches_dir.files():
        file_path_i = sys_prefix.joinpath(patch_file_i.lines()[0]
                                          .strip()).realpath()
        if not file_path_i.isfile():
            print('File to patch not found: `%s`' % file_path_i,
                  file=sys.stderr)
            continue
        process_i = sp.Popen(['patch', '-d', file_path_i.parent,
                              file_path_i.name, '-i', patch_file_i,
                              '-t',  # Ask no questions
                              '-N',  # Ignore patches that appear to be
                                     # reversed or already applied.
                             ], shell=True)
        process_i.wait()


# `__init__.py` is missing for:
#  - [`google` module in `google.protobuf`][1].
#  - `ruamel` module in `ruamel.yaml`
#  - `pyutilib`
#
# [1]: http://www.py2exe.org/index.cgi/GoogleProtobuf
DEFAULT_TOUCH_INIT = {'pyutilib.component.core': ['pyutilib',
                                                  'pyutilib.component'],
                      'protobuf': ['google'],
                      'ruamel.yaml': ['ruamel']}


def fix_init(package_specs, package_inits=None):
    site_packages = ph.path([p for p in site.getsitepackages()
                             if p.endswith('site-packages')][0])
    package_inits = package_inits or DEFAULT_TOUCH_INIT

    for package_spec_i in package_specs:
        name_i = re.split(r'=+', package_spec_i)[0]
        if name_i in package_inits:
            for missing_init_i in package_inits[name_i]:
                init_i = site_packages.joinpath(*(missing_init_i.split('.') +
                                                  ['__init__.py']))
                if not init_i.isfile():
                    print('Created missing `%s`.' % init_i)
                    init_i.touch()


# Apply default patches on import.
apply_patches()
