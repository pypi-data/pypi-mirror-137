server_type = 'dictionary'

import os
import pkgutil
import sys

if server_type == 'feeds':
    api = 'gracie_feeds_api.'
    from gracie_feeds_api.GracieErrors import gracieAPIClassLoaderErrorException
elif server_type == 'dictionary':
    api = 'gracie_dictionary_api.'
    from gracie_dictionary_api.GracieErrors import gracieAPIClassLoaderErrorException
else:
    raise BaseException('Unknown server type %s' % server_type)


class GracieApiClassLoader(gracieAPIClassLoaderErrorException):
    controller_classes = {}
    _class_directory = None
    _gracie = None

    def __init__(self, class_directory, gracie):
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), class_directory)):
            raise gracieAPIClassLoaderErrorException('Class directory does not exist', class_directory)

        self._class_directory = class_directory
        self._gracie = gracie

    def load_classes(self):
        self._load_classes(self._class_directory, self._gracie)

    def get_controller_classes(self):
        return self.controller_classes

    def _load_classes(self, class_directory, gracie):
        modules = pkgutil.iter_modules(path=[os.path.join(os.path.dirname(os.path.abspath(__file__)), class_directory)])

        for loader, mod_name, ispkg in modules:
            if mod_name not in sys.modules:
                loaded_mod = __import__(api + class_directory + "." + mod_name, fromlist=[mod_name], globals=globals())
                loaded_class = getattr(loaded_mod, mod_name)
                loaded_class_inst = loaded_class(gracie)
                self.controller_classes.update({mod_name: loaded_class_inst})

    def load_class(self, mod_name):
        loaded_mod = __import__(api + self._class_directory + "." + mod_name, fromlist=[mod_name], globals=globals())
        loaded_class = getattr(loaded_mod, mod_name)
        return loaded_class(self._gracie)
