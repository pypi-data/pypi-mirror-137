import importlib

def check_module_version(version=1, file_name=""):
    version_func = None
    try:
        if version < 0:
            return 0, "Version 0 reached, no matched function"
        version_func = importlib.import_module('versions.v{}.{}'.format(version, file_name))
    except ModuleNotFoundError as e:
        version_func, version = check_module_version(version=version-1, file_name=file_name)
    return version_func, version

def get_floorplans(version=1):
    # Check if module is valid by its version
    valid_module, version = check_module_version(version,"floorplan")
    # If look up process is done and ended up with no match result
    if not valid_module:
        result = "No module match with requested version"
    else:
        try:
            # Get the data by its function
            result = valid_module.get_floorplans()
        except AttributeError:
            # Check another version if the function is not exist in module
            result = get_floorplans(version=version-1)
    return result

def get_routes(version=1):
    valid_module, version = check_module_version(version,"floorplan")
    try:
        result = valid_module.get_routes()
    except AttributeError:
        result = get_routes(version=version-1)
    return result

def get_agendas(version=1):
    valid_module, version = check_module_version(version,"agenda")
    try:
        result = valid_module.get_agenda_list_view()
    except AttributeError:
        result = get_agendas(version=version-1)
    return result

def get_session(version=1):
    valid_module, version = check_module_version(version,"agenda")
    try:
        result = valid_module.get_agenda_session()
    except AttributeError:
        result = get_session(version=version-1)
    return result
