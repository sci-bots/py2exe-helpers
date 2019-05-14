'''
Modules to include by default.
'''
import re

__all__ = ['DEFAULT_INCLUDES', 'DEFAULT_PACKAGES', 'get_includes',
           'get_packages']

DEFAULT_INCLUDES = {'scons': ['UserDict',
                              'UserList',
                              'UserString'],
                    'platformio-tool-scons': ['UserDict',
                                              'UserList',
                                              'UserString'],
                    'dmf-device-ui': ['dmf_device_ui.bin.device_view'],
                    'pygtk2': ['atk', 'cairo', 'gio', 'pango', 'pangocairo'],
                    'matplotlib': ['cycler',
                                   'matplotlib.backends.backend_gtkagg',
                                   'matplotlib.backends.backend_wxagg',
                                   'matplotlib'],
                    'microdrop.dmf-device-ui-plugin': ['dmf_device_ui_plugin'],
                    'microdrop.dropbot-plugin': ['dropbot_plugin'],
                    'microdrop': ['microdrop.microdrop',
                                  'win32com.shell'],
                    'protobuf': ['google.protobuf.descriptor']}

DEFAULT_PACKAGES = {'IPython': ['IPython'],
                    'dropbot': ['dropbot'],
                    'jsonpickle': ['jsonpickle'],
                    'jupyter_core': ['jupyter_core'],
                    'lxml': ['lxml'],
                    'numpy': ['numpy'],
                    'pandas': ['pandas'],
                    'setuptools': ['pkg_resources'],
                    'platformio': ['platformio'],
                    'pytables': ['tables'],
                    'trollius': ['trollius'],
                    'zmq': ['zmq']}

def get_includes(package_specs, package_includes=None):
    '''
    Parameters
    ----------
    package_specs : list[str]
        List of Conda package specifiers, e.g., from the dependencies section
        of a Conda environment YAML file.
    package_includes : dict[str->list[str]]
        Mapping from Conda package name to list of module includes.

    Returns
    -------
    list[str]
        List of modules to explicitly include in the py2exe distribution.
    '''
    package_includes = package_includes or DEFAULT_INCLUDES
    return [include_ij for dependency_i in package_specs
            for include_ij in
            package_includes.get(re.split(r'=+', dependency_i)[0], [])]


def get_packages(package_specs, package_packages=None):
    '''
    Parameters
    ----------
    package_specs : list[str]
        List of Conda package specifiers, e.g., from the dependencies section
        of a Conda environment YAML file.
    package_packages : dict[str->list[str]]
        Mapping from Conda package name to list of required complete packages
        (as opposed to only modules within package automatically detected by
        ``py2exe`` module finder).

    Returns
    -------
    list[str]
        List of full Python packages to explicitly include in the py2exe
        distribution.
    '''
    package_packages = package_packages or DEFAULT_PACKAGES
    return [package_ij for dependency_i in package_specs
            for package_ij in
            package_packages.get(re.split(r'=+', dependency_i)[0], [])]
