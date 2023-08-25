from flask import render_template, redirect, url_for, flash, session, request, send_file
from flask_login import current_user, login_user
from flask.views import MethodView
from forms import SignupForm, LoginForm, EmployeeEditForm
from api_service import *
from decor import token_required
from flask_jwt_extended import jwt_required
from config import STORAGE_PATH


def home():
    """
    URL: / or /home
    Description: Home page of the application.
    """
    return render_template('home.html')


class LoginView(MethodView):
    """
    URL: /login
    Description: User login page allowing GET (rendering) and POST (authentication) methods.
    """
    def get(self):
        form = LoginForm()
        return render_template('login.html', form=form)
    
    def post(self):
        try:
            form = LoginForm()
            if form.validate_on_submit():
                email_or_phone = form.data["email_or_phone"]
                passw = form.data["password"]
                res = login_api({
                    "email_or_phone": email_or_phone,
                    "password": passw
                })
                if "error" in res:
                    flash(f"Failed to login {res['error']}", "danger")
                else:
                    token = res["data"]["token"]
                    flash(f"successfully loggedin", "success")
                    session['access_token'] = token
                    return redirect(url_for("home_url.dashboard"))
            else:
                flash("Please correct the following errors and try again", "danger")
            return render_template('login.html', form=form)
        except Exception as err:
            print(err)
            flash(f"Error: {err}", "danger")
            return render_template('login.html', form=form)
        

class LogoutView(MethodView):
    decorators = [token_required]

    def get(self):
        res = logout_api()
        if res["status_code"] == 200:
            print("logout successfully")
            del session["access_token"]
            del session["user_role"]
        return redirect(url_for("home_url.login"))
            

class AddEmployeeView(MethodView):
    """
    URL: /employee/add
    Description: Page for adding a new employee, available through GET (rendering) and POST (employee creation) methods.
    """
    decorators = [token_required]

    def get(self):
        form = SignupForm()
        return render_template('create.html', form=form)
    
    def post(self):
        try:
            form = SignupForm()
            if form.validate_on_submit():
                form_data = form.data
                del form_data["submit"], form_data["csrf_token"], form_data["confirm"]
                res = create_emp_api(form_data)
                if "error" in res:
                    flash(f"Failed to create the employee, {res['error']}", "danger")
                elif res["status_code"] == 201:
                    flash(f"Employee created successfully", "success")
                    return redirect(url_for("home_url.dashboard"))
            else:
                flash("Please correct the following errors and try again", "danger")
            return render_template('create.html', form=form)
        except Exception as err:
            print(err)
            flash(f"Error: {err}", "danger")
            return render_template('create.html', form=form)
        

class DashboardView(MethodView):
    """
    URL: /dashboard
    Description: Dashboard page displaying Employees information based on the role, accessible through a GET request.
    """
    decorators = [token_required]

    def get(self):
        is_admin = False
        role = ""
        my_data = get_current_user_api()
        if "error" in my_data:
            flash("failed to fetch current user data", "danger")
            my_data = {}
        else:
            my_data = my_data["data"]
            role = my_data["role"][0]
            session["user_role"] = role

        roles = get_all_roles()
        if roles["status_code"] == 200:
            roles = roles["data"]["roles"]
        else:
            roles = []
        selected_role = request.args.get('role')
        filters = {}
        if selected_role:
            filters.update({"roles":selected_role})
        # If a role is selected, query the database with the role filter
        # if selected_role:
        #     users = collection.find({'role': selected_role})
        # else:
        #     users = collection.find()
        res = get_all_users_api(filters=filters)
        if res and res["status_code"] == 403:#permission only for get
            users_data = {}
        else:
            users_data = res["data"]
        return render_template('dashboard.html', users = users_data, current_user=my_data, roles=roles, selected_role=selected_role)
    

class ViewEmployeeView(MethodView):
    """
    URL: /employee/view/<id>
    Description: Page to view details of a specific employee, accessed via a GET request.
    URL Parameters:
    - id: ID of the employee whose details are being viewed.
    """
    decorators = [token_required]

    def get(self, id):
        res = get_all_users_api(id)
        if res and res["status_code"] == 403:#permission only for get
            user_data = {}
        else:
            user_data = res["data"]
        return render_template('details.html', user = user_data, user_id=id)
    

class EditEmployeeView(MethodView):
    """
    URL: /employee/edit/<id>
    Description: Page for editing employee details, accessible through GET (rendering) and POST (employee details update) methods.
    URL Parameters:
    - id: ID of the employee whose details are being edited.
    """
    decorators = [token_required]

    def get(self, id):
        res = get_all_users_api(id)
        if res and res["status_code"] == 403:#permission only for get
            flash("You dont have permission to do this", "danger")
            return redirect(url_for("home_url.dashboard"))
        else:
            user_data = res["data"]
            form = EmployeeEditForm(**user_data)
        return render_template('edit.html', form=form, user_id=id)
    
    def post(self, id):
        try:
            form = EmployeeEditForm()
            if form.validate_on_submit():
                form_data = form.data
                del form_data["submit"], form_data["csrf_token"]
                res = edit_employee_api(id, form_data)
                if "error" in res:
                    flash(f"Failed to edit the employee, {res['error']}", "danger")
                elif res["status_code"] == 204:
                    flash(f"Employee details updated successfully", "success")
                    return redirect(url_for("home_url.dashboard"))
            else:
                flash("Please correct the following errors and try again", "danger")
            return render_template('edit.html', form=form, user_id=id)
        except Exception as err:
            print(err)
            flash(f"Error: {err}", "danger")
            return render_template('edit.html', form=form, user_id=id)
        

class DeleteEmployeeView(MethodView):
    """
    URL: /employee/delete/<id>
    Description: Page for deleting an employee, available through a GET request.
    URL Parameters:
    - id: ID of the employee to be deleted.
    """
    decorators = [token_required]

    def get(self, id):
        res = delete_employee_api(id)
        if res["status_code"] == 204:
            flash(f"Employee Deleted successfully", "success")
        elif res["status_code"] == 403:
            flash("You dont have permission to do this", "danger")
        else:
            flash(f"Something went wrong", "danger")
        return redirect(url_for("home_url.dashboard"))
    

class ExportEmployeeView(MethodView):
    """
    URL: /employee/export/<id>/<type>
    Description: Page to export employee details in various formats (CSV, XLSX, JSON), accessible via a GET request.
    URL Parameters:
    - id: ID of the employee whose details are being exported.
    - type: Format in which to export data (csv, xlsx, json).
    """
    decorators = [token_required]

    def get(self, id, type):
        res = export_employee_api(id, type)
        if res["status_code"] == 200:
            file_name = f'{STORAGE_PATH}/user_details.{type}'
            return send_file(file_name, as_attachment=True)
        return redirect(url_for("home_url.dashboard"))
    
