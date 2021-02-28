from flask import Flask,render_template,request, redirect, flash,url_for
from flask_security.decorators import roles_accepted,roles_required
from flask_security.utils import hash_password,current_user
from models import db,User,Role,Game
from forms import GameUploadForm
from flask_wtf.file import FileRequired
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
    return render_template('base.html')

@app.route('/game/new',methods=['GET','POST'])
@roles_accepted('Game Developer')
def upload_new_game():
    error_message = None
    form = GameUploadForm()
    if request.method == 'POST' and form.validate(extra_validators={'game_rom':[FileRequired()]}):
        try:
            #convert file to hex text format
            rom_binary = form.game_rom.data.stream.read()
            title = form.title.data
            description = form.description.data
            game_entry = Game(title=title,description=description,file=rom_binary,user=current_user)
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

#TODO add in code to handle admins as well
@app.route('/game/update/<int:id>',methods=['GET','POST'])
@roles_accepted('Game Developer')
def update_game(id):
    game = Game.query.get(id)
    #handle case game not found
    if game is None:
        flash('The game you are trying to edit could not be found.')
        return redirect(url_for('index'))
    #redirect user if not owner
    if game.user.id != current_user.id:
        flash('You do not have permission to edit this game.')
        return redirect(url_for("/"))
    error_message = None
    form = GameUploadForm()
    if request.method == 'POST':
        if form.validate():
            try:
                #convert file to hex text format
                rom_binary = None
                if form.game_rom.data:
                    rom_binary = form.game_rom.data.stream.read()
                game.title = form.title.data
                game.description = form.description.data
                game.file = rom_binary
                db.session.commit()
            except IOError:
                error_message = "Failed to save file."
            except SQLAlchemyError:
                error_message = 'Failed to store file in database.'
                #remove saved file
            else:
                return game.filename
    #populate form with data from database            
    else:
        form.title.data = game.title
        form.description.data = game.description
    return render_template('upload_form.html',form=form,error_message=error_message,id=game.id)

@app.route('/game/<int:id>')
def game_profile(id):
    game = Game.query.get(id)
    print(game)
    if not game:
        #TODO Switch to redirect to listing page
        flash('The game you are searching for was not found.')
        return render_template('profile.html',game=game),404
    return render_template('profile.html',game=game)


if __name__ == "__main__":
    app.run(debug=True)