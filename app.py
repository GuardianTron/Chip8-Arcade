from flask import Flask,render_template,request
from flask_security.decorators import roles_accepted,roles_required
from flask_security.utils import hash_password,current_user
from models import db,User,Role,Game
from forms import GameUploadForm
from sqlalchemy.exc import SQLAlchemyError
from flask_migrate import Migrate
from flask_security import Security,SQLAlchemyUserDatastore
import os
import uuid

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

@app.route("/")
def index():
    roles = ''
    for role in current_user.roles:
        roles += f'{role.role} '
    return roles

@app.route('/game/new',methods=['GET','POST'])
@roles_accepted('Game Developer')
def upload_new_game():
    error_message = None
    form = GameUploadForm()
    if request.method == 'POST' and form.validate():
        try:
            #convert file to hex text format
            rom_binary = form.game_rom.data.stream.read()
            game_entry = Game(title='Test Title',description='Da game, duh',file=rom_binary,user=current_user)
            db.session.add(game_entry)
            db.session.commit()
        except IOError:
            error_message = "Failed to save file."
        except SQLAlchemyError:
            error_message = 'Failed to store file in database.'
            #remove saved file
        else:
            return game_entry.filename
        
    return render_template('upload_form.html',form=form,error_message=error_message)



if __name__ == "__main__":
    app.run(debug=True)