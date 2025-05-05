import importlib
import pkgutil

def load_all_subscribers():
    """Auto Load any Subscribers defined in this directory"""

    print("Loading subscribers")

    for _, module_name, _ in pkgutil.iter_modules(__path__):        
        importlib.import_module(f"{__name__}.{module_name}")