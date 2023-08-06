import importlib
import inspect
import os
import sys

def load(clazz, directories=[]):
    modules = []
    for directory in directories:
        abspath = os.path.abspath(directory)
        sys.path.append(abspath)
        for candidate in os.listdir(directory):
            if candidate == '__init__.py' or candidate[-3:] != '.py':
                continue
            path_modules = importlib.import_module(candidate[:-3])

            for name, obj in inspect.getmembers(path_modules):
                if inspect.isclass(obj) and obj:
                    try:
                        instance = getattr(path_modules, name)()
                        for super_class in instance.__class__.__bases__:
                            if super_class.__name__ == clazz.__name__:
                                modules.append(instance)
                                continue
                    except Exception as e:
                        continue

    return modules
