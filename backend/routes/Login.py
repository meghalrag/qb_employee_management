import datetime

# Import from system libraries
from flask import request, Response, json
from flask_jwt_extended import create_access_token, get_raw_jwt, jwt_required
from flask_restful import Resource
from mongoengine import DoesNotExist

# Import from application modules
from errors import UnauthorizedError, InternalServerError
from models.User import User, TokenBlacklist


# Class Login API to load in Routes
class LoginApi(Resource):
    """
    Endpoint: api/login
    Method: POST
    Description: Authenticate a user and generate a session token for API access.
    Request Body:
    - email_or_phone: (string) User's email/phone number.
    - password: (string) User's password.
    Response:
    - 200 OK: Successful authentication. Returns a session token.
    - 401 Unauthorized: Invalid credentials.
    """
    def post(self):
        try:
            # get body (json) from client request
            body = request.get_json()
            # get user object from database with condition username from request
            try:
                user = User.objects.get(username=body.get('email_or_phone'))
            except DoesNotExist:
                user = User.objects.get(phone_number=body.get('email_or_phone'))
            # check password (encryption)
            authorized = user.check_password_hash(body.get('password'))
            # if check password (decryption) failed raise Error with code UnauthorizedError
            if not authorized:
                raise UnauthorizedError
            # giving expire times for login
            expires = datetime.timedelta(days=1)
            # create access token with utility from flask-jwt-extended
            access_token = create_access_token(identity=user, expires_delta=expires)
            # response client with token and status code
            return {'token': access_token}, 200
        # if request failed or does not meet specifications
        except (UnauthorizedError, DoesNotExist):
            return {"error": "UnauthorizedError"}, 401 
        except Exception as e:
            return {"error": "InternalServerError"}, 500
        

class LogoutAPI(Resource):
    """
    Endpoint: api/logout
    Method: POST
    Description: Invalidate the current session token, logging out the user.
    Request Headers:
    - Authorization: (string) Session token.
    Response:
    - 200 OK: Logout successful.
    - 401 Unauthorized: Invalid session token.
    """
    @jwt_required
    def post(self):
        try:
            jti = get_raw_jwt()['jti']
            token = TokenBlacklist(jti=jti)
            token.save()
            return Response(json.dumps({"message":'Logout Successfully'}), mimetype='application/json', status=200)
        except Exception as err:
            return "Internal Server Error", 500
