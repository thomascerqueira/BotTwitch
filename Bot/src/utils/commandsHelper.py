def module_load(module_path):
        import importlib.util
        import sys
        
        try:
            module_name = module_path.split("/")[-1].split(".")[0]  # Récupère le nom du module sans l'extension
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            print(f"Module {module_name} chargé avec succès.")
            return module
        except Exception as e:
            print(f"Impossible de charger le module {module_path}. Erreur : {e}")
            
def getClassFromModule(module):
    print_help_class = None
    
    for name in dir(module):
        obj = getattr(module, name)
        if hasattr(obj, '__class__') and hasattr(obj, '__dict__'):
            print_help_class = obj
            break
        
    if not print_help_class:
        raise Exception(f"Impossible de trouver la classe dans le module {module}")
    
    return print_help_class