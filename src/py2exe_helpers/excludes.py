'''
Modules to exclude by default.
'''
import re
import sys

__all__ = ['DEFAULT_EXCLUDES', 'get_excludes', 'get_dll_excludes']

DEFAULT_EXCLUDES = {}

DEFAULT_DLL_EXCLUDES = {'__core__':
                        # Work around 'api-ms-win-core-registry-l1-1-0.dll' not
                        # found: https://stackoverflow.com/a/40090641/345236
                        ['ADVAPI32.dll',
                         'CFGMGR32.dll',
                         'CRYPT32.dll',
                         'GDI32.dll',
                         'IPHLPAPI.DLL',
                         'KERNEL32.dll',
                         'MPR.dll',
                         'MSIMG32.dll',
                         'MSVCP120.dll',
                         'MSVCP90.dll',
                         'MSVCR120.dll',
                         'MSVCR90.dll',
                         'NSI.dll',
                         'POWRPROF.dll',
                         'PSAPI.dll',
                         'SHFOLDER.dll',
                         'Secur32.dll',
                         'USER32.dll',
                         'WINNSI.DLL',
                         'WINSTA.dll',
                         'WTSAPI32.dll',
                         'MSVFW32.dll',
                         'AVIFIL32.dll',
                         'AVICAP32.dll',
                         'ADVAPI32.dll',
                         'CRYPT32.dll',
                         'WLDAP32.dll']}

if not (sys.version_info.major >= 3 and sys.version_info.minor >= 5):
    # No support for `async`/`await`.  See [here][1].
    #
    # [1]: https://realpython.com/async-io-python/#python-version-specifics
    DEFAULT_EXCLUDES.update({'asyncserial': ['asyncserial._asyncpy3'],
                             'base-node-rpc': ['base_node_rpc._async_py36'],
                             'conda-helpers': ['conda_helpers._async_py35'],
                             'jinja2': ['jinja2.asyncsupport']})


def get_excludes(package_specs, package_excludes=None):
    '''
    Parameters
    ----------
    package_specs : list[str]
        List of Conda package specifiers, e.g., from the dependencies section
        of a Conda environment YAML file.
    package_excludes : dict[str->list[str]]
        Mapping from Conda package name to list of module excludes.

    Returns
    -------
    list[str]
        List of modules to explicitly exclude from the py2exe distribution.
    '''
    package_excludes = package_excludes or DEFAULT_EXCLUDES
    return [exclude_ij for dependency_i in package_specs
            for exclude_ij in
            package_excludes.get(re.split(r'=+', dependency_i)[0], [])]


def get_dll_excludes(package_specs, package_dll_excludes=None):
    '''
    Parameters
    ----------
    package_specs : list[str]
        List of Conda package specifiers, e.g., from the dependencies section
        of a Conda environment YAML file.
    package_dll_excludes : dict[str->list[str]]
        Mapping from Conda package name to list of DLL excludes.

    Returns
    -------
    list[str]
        List of DLL names to explicitly exclude from the py2exe distribution.
    '''
    package_dll_excludes = package_dll_excludes or DEFAULT_DLL_EXCLUDES
    dll_excludes = DEFAULT_DLL_EXCLUDES['__core__']
    dll_excludes += [exclude_ij for dependency_i in package_specs
                     for exclude_ij in package_dll_excludes
                     .get(re.split(r'=+', dependency_i)[0], [])]
    return dll_excludes
