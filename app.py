from flask import Flask
from models import db,User,Role
from flask_migrate import Migrate
from flask_security import Security,SQLAlchemyUserDatastore

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

db.init_app(app)
migrate = Migrate(app,db)
user_datastore = SQLAlchemyUserDatastore(db,User, Role)
security = Security(app,user_datastore)


if __name__ == "__main__":
    app.run(debug=True)