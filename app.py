from flask import Flask
from config import Config
from extensions import mysql
from routes.routes import routes as routes_blueprint

app = Flask(__name__)
app.config.from_object(Config)

mysql.init_app(app)

app.register_blueprint(routes_blueprint)

if __name__ == "__main__":
    app.run(debug=True)

