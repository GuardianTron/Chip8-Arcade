from flask import Flask,render_template,request, redirect, flash,url_for,json,abort,send_file
from flask import Markup,escape
from flask_security.decorators import roles_accepted,roles_required
from flask_security.utils import hash_password,current_user
from models import db,User,Role,Game,ControlConfig
from forms import GameUploadForm
from flask_wtf.file import FileRequired
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.exc import SQLAlchemyError
from flask_migrate import Migrate
from flask_security import Security,SQLAlchemyUserDatastore
import os
import uuid

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
csrf = CSRFProtect(app)

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

#TODO Create a proper 404 page
@app.route("/game/play/<int:id>")
def play_game(id):
    game = Game.query.get(id)
    if game is None:
        flash('The game you are looking for could not be found.')
        return "The game you are searching for could not be found",404
    return render_template("play.html",game=game)

@app.route('/game/new',methods=['GET','POST'])
@roles_accepted('Game Developer')
def upload_new_game():
    form = GameUploadForm()
    if request.method == 'POST' and form.validate(extra_validators={'game_rom':[FileRequired()]}):
        try:
            #convert file to hex text format
            rom_binary = form.game_rom.data.stream.read()
            title = form.title.data
            description = form.description.data
            instructions = form.instructions.data
            game_entry = Game(title=title,description=description,instructions=instructions,file=rom_binary,user=current_user)
            game_entry.control_config.append(ControlConfig(key_mapping=form.key_configuration))
            db.session.add(game_entry)
            db.session.commit()
        except IOError:
            flash("Failed to save file.")
        except SQLAlchemyError:
            flash('Failed to store file in database.')
            #remove saved file
        else:
            flash('Your game has been successfully uploaded.')
            return redirect(url_for('game_profile',id=game_entry.id))
        
    return render_template('upload_form.html',form=form)

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
    form = GameUploadForm(obj=game)

    if request.method == 'POST':
        if form.validate():
            try:
                #convert file to hex text format
                rom_binary = None
                if form.game_rom.data:
                    rom_binary = form.game_rom.data.stream.read()
                game.title = form.title.data
                game.description = form.description.data
                game.instructions = form.instructions.data
                game.file = rom_binary

                #update control configuration
                #add new configuration if prior config not specified
                config = game.control_config.first()
                if config :
                    config.key_mapping = form.key_configuration
                else:
                    game.control_config.append(ControlConfig(key_mapping=form.key_configuration))
                
                db.session.commit()
            except IOError:
                flash("Failed to save file.")
            except SQLAlchemyError:
                flash('Failed to store file in database.')
                #remove saved file
            else:
                flash("Your game has been successfully updated.")
                return redirect(url_for('game_profile',id=game.id))
    #populate form with data from database       
    else:
        #form.title.data = game.title
        #form.description.data = game.description
        config = game.control_config.first()
        if config:
            form.key_configuration = config.key_mapping

    return render_template('upload_form.html',form=form,id=game.id)

@app.route('/game/config/<int:id>')
def game_json(id):
    game = Game.query.get(id)
    if game is None:
        return json.jsonify({"error":"The game could not be found."})
    control_config = game.control_config.first()
    if control_config is None:
        return json.jsonify({"error":"Could not find control configuration for the game."})
    game_info = {}
    game_info['rom'] = url_for('send_rom',id=id)
    game_info['chip8_font'] = url_for('static',filename="javascript/emulator/fonts/chip8.cft")
    game_info['super_chip_font'] = url_for('static',filename="javascript/emulator/fonts/chip8super.sft")
    #reverse keymapping to fit with emulator standard of hex_value:key
    keys_remapped = {control_config.key_mapping[key_code]:key_code for key_code in control_config.key_mapping}
    game_info['key_config'] = keys_remapped
    return json.jsonify(game_info)
    
@app.route('/game/rom/<int:id>')
def send_rom(id):
    game = Game.query.get(id)
    if game is None:
        abort(404)
    try:
        return send_file(game.path)
    except:
        abort(404)
@app.route('/game/<int:id>')
def game_profile(id):
    game = Game.query.get(id)
    if not game:
        #TODO Switch to redirect to listing page
        flash('The game you are searching for was not found.')
        return render_template('profile.html',game=game),404
    return render_template('profile.html',game=game)

@app.route('/game/mygames')
@roles_accepted('Game Developer')
def list_games_developer():
    page = request.args.get('page',default=1,type=int)
    posts_per_page = app.config['POSTS_PER_PAGE']
    games = Game.query.filter(User.id == current_user.id).order_by(Game.created_on.desc()).paginate(page,posts_per_page,False)
    return render_template('game_list_dev.html',games=games.items,paginator=games)

@app.route('/game/delete',methods=["POST"])
@roles_accepted('Game Developer')
def delete_games():
    ids = request.form.getlist('game_ids')
    games = Game.query.filter(Game.id.in_(ids),User.id==current_user.id).all()
    for game in games:
        db.session.delete(game)
    db.session.commit()
    flash('Your games have been deleted.')
    return redirect(url_for('list_games_developer'))

@app.route('/games')
def list_games():
    page = request.args.get('page',default=1,type=int)
    posts_per_page = app.config['POSTS_PER_PAGE']
    games = Game.query.order_by(Game.created_on.desc()).paginate(page,posts_per_page,False)
    return render_template('game_list.html',games=games.items,paginator=games)

@app.template_filter('newline_to_p')
def newLineToParagragh(string):
    lines_raw = string.splitlines()
    lines_sanitized = [Markup.escape(line) for line in lines_raw]
    return Markup(f"<p>{'</p><p>'.join(lines_sanitized)}</p>")


if __name__ == "__main__":
    app.run(debug=True)