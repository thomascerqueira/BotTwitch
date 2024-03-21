from src.logger.logger import logger

def module_load(module_path):
        import importlib.util
        import sys
        
        try:
            module_name = module_path.split("/")[-1].split(".")[0]  # Récupère le nom du module sans l'extension
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            logger.info(f"Module {module_name} successfully loaded from {module_path}")
            return module
        except Exception as e:
            logger.error(f"Impossible to load module from {module_path}. Erreur : {e}")
            
def getClassFromModule(module):
    print_help_class = None
    
    for name in dir(module):
        obj = getattr(module, name)
        if hasattr(obj, '__class__') and hasattr(obj, '__dict__'):
            print_help_class = obj
            break
        
    if not print_help_class:
        raise Exception(f"Impossible to find the class in {module}")
    
    return print_help_class