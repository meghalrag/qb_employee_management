### Backend

make backend folder as your base directory by moving to backend folder from terminal

```
cd backend
```

Installing all libraries needed by this project using [pip](https://pypi.org/project/pip/).
```
pip install -r requirements.txt
```

Make a configuration file with name *.env* with this configuration (_change as desired_).
```
MONGODB_SETTINGS = { 'host': 'mongodb://localhost/EMPLOYEE MANAGEMENT' }
JWT_SECRET_KEY = 'employeemanagementwillnotbreach'
```

Setting the environment for this project.
```
export FLASK_APP=app.py
export ENV_FILE_LOCATION=./.env
``` 

Running the project.
```
flask run --port 5000
```

### Testing

To test the api endpoint that has been created you can use **curl** utility. Before test, you must login
first to get jwt token and using it in every request header you sent.

```
curl -X POST localhost:5000/api/login -d '{"username":"manager@123.com", "password":"123"}' -H "Content-Type: application/json"
```

### Swagger UI

You can find the swagger documentation of the api endpoints here:

```
http://127.0.0.1:5000/api/docs
```