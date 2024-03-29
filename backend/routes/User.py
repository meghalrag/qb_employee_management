from flask import Response, request, json
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_restful import Resource
from mongoengine import FieldDoesNotExist, NotUniqueError, DoesNotExist, InvalidQueryError

from errors import NoAuthorizationError, InternalServerError, SchemaValidationError, EmailAlreadyExistsError, \
    DeletingUserError, UpdatingUserError
from models.User import User, UserProfile, UserFileMapping
from common.export_helper import export_to_csv_and_save, export_to_json_and_save, export_to_xlsx_and_save


class User2Api(Resource):
    @jwt_required
    def get(self):
        """
        Endpoint: api/user
        Method: GET
        Description: Retrieve a list of all employee users.
        Response:
        - 200 OK: Successful. Returns a list of employee users with their details.
        - 401 Unauthorized: No Authorization Error.
        - 500 Internal Server Error: All other errors.
        """
        res = []
        try:
            filters = request.get_json()
            if filters:
                users = User.objects.filter(**filters)
                users = UserProfile.objects.filter(user__in=users)
            else:
                users = UserProfile.objects.all()
            for each in users:
                temp = {}
                temp["user_id"] = str(each.user.id)
                temp["emp_id"] = str(each.user.emp_id)
                temp["role"] = each.user.roles[0]
                temp["name"] = each.name
                temp["email"] = each.email
                temp["phone_number"] = each.phone_number
                temp["designation"] = each.designation
                temp["department"] = each.department
                temp["manager"] = each.manager
                temp["hired_date"] = str(each.hired_date)
                res.append(temp)
                del temp
            res = json.dumps(res)
            return Response(res, mimetype='application/json', status=200)
        except NoAuthorizationError:
            return {"error": "No Authorization Error"}, 401
        except Exception:
            return {"error": "Internal Server Error"}, 500

    @jwt_required
    def post(self):
        """
        Endpoint: api/user
        Method: POST
        Description: Create a new employee user.
        Request Body:
        - name: (string) Employee's name.
        - email: (string) Employee's email.
        - phone number: (string) Employee's phone.
        - password: (string) Employee's password.
        - designation: (string) Employee's designation.
        - department: (string) Employee's department.
        - manager: (string) Employee's manager.
        Response:
        - 201 Created: Employee creation successful.
        - 400 Bad Request: Schema Validation Error/Email/Phone Number AlreadyExists Error.
        - 500 Internal Server Error: All other errors.
        """
        try:
            body = request.get_json()
            user_schema = {
                "username": body["email"],
                "phone_number": body["phone_number"],
                "password": body["password"]
            }
            user = User(**user_schema)
            user.hash_password()
            user.emp_id = len(User.objects.all())+1
            user.save()
            del body["password"]
            user_profile = UserProfile(**body)
            user_profile.user = user
            user_profile.save()
            id = user.id
            del user, user_profile
            return {'id': str(id)}, 201
        except FieldDoesNotExist:
            return {"error": "Schema Validation Error"}, 400
        except NotUniqueError:
            return {"error": "Email/Phone Number AlreadyExists Error"}, 400
        except Exception:
            return {"error": "Internal Server Error"}, 500


class UserApi(Resource):
    @jwt_required
    def get(self, id):
        """
        Endpoint: api/user/<id>
        Method: GET
        Description: Retrieve the details of a perticular employee user.
        Response:
        - 200 OK: Successful. Returns a list of employee user with the details.
        """
        res = []
        try:
            user = User.objects().get(id=id)
            user_prof = UserProfile.objects.get(user=user)
            temp = {}
            temp["user_id"] = str(user_prof.user.id)
            temp["emp_id"] = str(user_prof.user.emp_id)
            temp["role"] = user_prof.user.roles[0]
            temp["name"] = user_prof.name
            temp["email"] = user_prof.email
            temp["phone_number"] = user_prof.phone_number
            temp["designation"] = user_prof.designation
            temp["department"] = user_prof.department
            temp["manager"] = user_prof.manager
            temp["hired_date"] = str(user_prof.hired_date)
            res = json.dumps(temp)
            return Response(res, mimetype='application/json', status=200)
        except DoesNotExist:
            return {"error": "User DoesNotExist with id"}, 500
        except Exception:
            return {"error": "Internal Server Error"}, 500
        
    @jwt_required
    def delete(self, id):
        """
        Endpoint: api/user/<id>
        Method: DELETE
        Description: Delete a specific employee user.
        URL Parameters:
        - id: (string) ID of the employee user to be deleted.
        Response:
        - 204 No Content: Deletion successful.
        - 404 Not Found: Employee user not found.
        """
        try:
            user = User.objects().get(id=id)
            UserProfile.objects.get(user=user).delete()
            user.delete()
            return Response(json.dumps({"message":'Deleted Successfully'}), mimetype='application/json', status=204)
        except DoesNotExist:
            return {"error": "DeletingUserError"}, 400
        except Exception:
            return {"error": "Internal Server Error"}, 500

    @jwt_required
    def put(self, id):
        """
        Endpoint: api/user/<id>
        Method: PUT
        Description: Update details of a specific employee user.
        URL Parameters:
        - id: (string) ID of the employee user to be updated.
        Request Body:
        - name: (string) Employee's name.
        - email: (string) Employee's email.
        - phone number: (string) Employee's phone.
        - designation: (string) Employee's designation.
        - department: (string) Employee's department.
        - manager: (string) Employee's manager.
        Response:
        - 204 No Content: Update successful.
        - 400 Bad Request: SchemaValidationError/UpdatingUserError.
        - 500 Internal Server Error: All other errors.
        """
        try:
            user = User.objects.get(id=id)
            body = request.get_json()
            UserProfile.objects.get(user=user).update(**body)
            return Response(json.dumps({"message":'Updated Successfully'}), mimetype='application/json', status=204)
        except SchemaValidationError as err:
            return {"error": "SchemaValidationError"}, 400
        except DoesNotExist:
            return {"error": "UpdatingUserError"}, 400
        except Exception:
            return {"error": "Internal Server Error"}, 500
        

class GetCurrentUserAPI(Resource):
    """
    Endpoint: api/user/me
    Method: GET
    Description: Retrieve the details of the loggedin user.
    Response:
    - 200 OK: Successful. Returns the details of loggedin user.
    """
    @jwt_required
    def get(self):
        try:
            user_obj = User.objects.get(username=get_jwt_identity())
            res = {}
            res["user_id"] = str(user_obj.id)
            res["email"] = user_obj.username
            res["phone_number"] = user_obj.phone_number
            res["role"] = user_obj.roles
            res = json.dumps(res)
            return Response(res, status=200)
        except Exception as err:
            return {"error": "Internal Server Error"}, 500
        

class ExportEmpDataAPI(Resource):
    """
    Endpoint: api/user/export/<id>/<type>
    Method: GET
    Description: Export employee details in various formats (CSV, XLSX, JSON).
    URL Parameters:
    - id: (string) ID of the employee user whose details are to be exported.
    - type: (string) Format in which to export data (csv, xlsx, json).
    Response:
    - 200 OK: Export successful. Returns the employee details in the specified format.
    - 500 Internal: Employee export error.
    """
    @jwt_required
    def get(self, id, type):
        try:
            user_data = User.objects.get(id=id)
            prof = UserProfile.objects.get(user=user_data) 
            if type == "csv":
                file_id = export_to_csv_and_save(prof)
            elif type == "xlsx":
                file_id = export_to_xlsx_and_save(prof)
            else:
                file_id = export_to_json_and_save(prof)
            UserFileMapping(user=user_data, file_id=str(file_id)).save()
            return {"message": "Data Exported Successfully"}, 200
        except Exception as err:
            return {"error": "Internal Server Error"}, 500
        

class GetAllRolesAPI(Resource):
    """
    Endpoint: api/roles
    Method: GET
    Description: Retrieve all the roles.
    Response:
    - 200 OK: Successful. Returns list of roles available in the applicaion.
    - 500 Internal: All errors.
    """
    @jwt_required
    def get(self):
        from middleware.casbin_middleware import casbin_enforcer
        try:
            roles = list(set(casbin_enforcer.get_all_named_subjects("p")))
            return {"roles": roles}, 200
        except Exception as err:
            return {"error": "Internal Server Error"}, 500
