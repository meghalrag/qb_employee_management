# Import from application modules
from routes.Login import LoginApi, LogoutAPI
from routes.User import User2Api, UserApi, GetCurrentUserAPI, ExportEmpDataAPI, GetAllRolesAPI


# Function to initialize route to API Flask
def initialize_routes(api):
    api.add_resource(LoginApi, '/api/login')
    api.add_resource(LogoutAPI, '/api/logout')
    api.add_resource(User2Api, '/api/user')
    api.add_resource(UserApi, '/api/user/<id>')
    api.add_resource(GetCurrentUserAPI, '/api/user/me')
    api.add_resource(ExportEmpDataAPI, '/api/user/export/<id>/<type>')
    api.add_resource(GetAllRolesAPI, '/api/roles')
