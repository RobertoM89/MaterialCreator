import platform
import MaterialCreator.material_creator as mc

if platform.python_version().startswith('2'):  
    reload(mc)
elif platform.python_version().startswith('3'):
    import importlib
    importlib.reload(mc)
    
mc.main()