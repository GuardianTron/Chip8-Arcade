from flask import Flask
from flask_security.decorators import roles_accepted
from flask_security.utils import hash_password,current_user
from models import db,User,Role
from flask_migrate import Migrate
from flask_security import Security,SQLAlchemyUserDatastore

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

db.init_app(app)
migrate = Migrate(app,db)
user_datastore = SQLAlchemyUserDatastore(db,User, Role)
security = Security(app,user_datastore)

#create test user
#TODO remove once signup is created
@app.before_first_request
def create_test_user():
    role = user_datastore.find_or_create_role(name='Game Developer',role='game_dev',description="A chip 8 game developer that can add, edit, and remove their own chip8 games and supply game specific configurations for the chip 8 virtual machine.")
    if not user_datastore.find_user(name="test_dev"):
        user = user_datastore.create_user(name='test_dev',email='test_dev@test.com',password=hash_password('password'))
        user_datastore.add_role_to_user(user,role)
    db.session.commit()


@app.route('/game/new')
@roles_accepted('game_dev')
def upload_new_game():
    pass



if __name__ == "__main__":
    app.run(debug=True)