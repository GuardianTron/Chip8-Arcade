from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileRequired
from wtforms import StringField,TextAreaField
from wtforms.validators import InputRequired, ValidationError,Length
from werkzeug.datastructures import FileStorage

class FileSize:
    def __init__(self,max_size,message=None):
         
        self.max_size = max_size
        if not message:
            #use max size for message
            prefix = ('','kilo','mega','giga')
            kilobyte = 2**10
            prefix_index = 0
            max_size_converted = max_size
            while max_size_converted > kilobyte and prefix_index < 4:
                max_size_converted /= kilobyte
                prefix_index += 1
            message = f"Files must be less than {max_size_converted} {prefix[prefix_index]}bytes in size."

        self.message = message
    
    def __call__(self,form,field):
        if field.data:
            if type(field.data) == bytes and len(field.data) > self.max_size:
                raise ValidationError(self.message)
            else:
                #get length by reading to end of stream
                start_pos = field.data.stream.tell()
                #seek to end
                field.data.stream.seek(start_pos,2)
                size = field.data.stream.tell()
                #set pointer back to start
                field.data.stream.seek(start_pos)
                if size > self.max_size:
                    raise ValidationError(self.message)


            

    

         

class GameUploadForm(FlaskForm):
    game_rom = FileField('game_rom',validators=[FileRequired(),FileSize(4*2**10)])
    title = StringField('Title',validators=[InputRequired(),Length(min=1,max=255)])
    description = TextAreaField('Description',validators=[InputRequired(),Length(min=1,max=5000)])