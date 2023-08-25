from flask import Flask
import urls


app = Flask(__name__)
app.config.update(dict(SECRET_KEY='xiaasdasdxcasdcsa'))
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

app.register_blueprint(urls.mod)

if __name__ == '__main__':
    # app.debug = True
    # app.run()
    app.run(debug=True, port=8000)