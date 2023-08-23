from flask import Blueprint
import views

# Create the blueprint for this app
mod = Blueprint("home_url", __name__, url_prefix="", template_folder="templates")

# Add the view as route; methods like GET, POST, PUT will automatically route to class methods with parameters
mod.add_url_rule('/', view_func=views.home)
mod.add_url_rule('/home', view_func=views.home)
mod.add_url_rule('/login', view_func=views.LoginView.as_view("login"), methods=["GET", "POST"])
mod.add_url_rule('/dashboard', view_func=views.DashboardView.as_view("dashboard"), methods=["GET"])
mod.add_url_rule('/employee/add', view_func=views.AddEmployeeView.as_view("add_employee"), methods=["GET", "POST"])
mod.add_url_rule('/employee/view/<id>', view_func=views.ViewEmployeeView.as_view("view_employee"), methods=["GET"])
mod.add_url_rule('/employee/edit/<id>', view_func=views.EditEmployeeView.as_view("edit_employee"), methods=["GET", "POST"])
mod.add_url_rule('/employee/delete/<id>', view_func=views.DeleteEmployeeView.as_view("delete_employee"), methods=["GET"])
mod.add_url_rule('/employee/export/<id>/<type>', view_func=views.ExportEmployeeView.as_view("export_employee"), methods=["GET"])
mod.add_url_rule('/logout', view_func=views.LogoutView.as_view("logout"), methods=["GET"])
# mod.add_url_rule('/user', view_func=views.UserView.as_view("user_view"), methods=["GET", "POST"])