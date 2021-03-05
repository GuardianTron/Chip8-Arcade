from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileRequired
from wtforms import StringField,TextAreaField,IntegerField,FieldList,FormField
from wtforms.fields.core import Field
from wtforms.validators import InputRequired, NumberRange, Regexp, ValidationError,Length,Optional
from werkzeug.datastructures import FileStorage
import re

'''
Validates the size of the file.
'''
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


class ConfigKeysUnique:
    def __init__(self,chip_key_field='hex_value',key_code_field='key_code',message=None):
        if not message:
            self.message = "Contains keycodes mapped to multiple Chip 8 keys."
            self.chip_key_field = chip_key_field
            self.key_code_field = key_code_field

    def __call__(self,form,field):
        key_codes = {}
        for entry in self.entries:
            if not hasattr(entry,self.chip_key_field):
                raise ValueError(f"{self.chip_key_field} is not a valid form attribute.")
            elif not hasattr(entry,self.key_code_field):
                raise ValueError(f"{self.key_code_field} is not a valid form attribute.")
            else:
                #make sure empty fields are not passed
                chip_key = str(getattr(entry,self.chip_key_field).data).strip()
                key_code = str(getattr(entry,self.key_code_field).data).strip()

                if chip_key and key_code:
                    if key_code in key_codes:
                        raise ValidationError(self.message)
                    else:
                        key_codes[key_code] = chip_key


            

def strip_whitespace(text):
    if text is not None:
        return text.strip()
    return text

class KeyConfigForm(FlaskForm):
    hex_value = StringField('Hex Value',validators=[Optional(),Regexp("^(0x)?[0-9a-f]$",re.IGNORECASE,message="Must be a hexidecimal value between 0 and F")])
    key_code = IntegerField('Key Code',validators=[Optional(),NumberRange(0,255,message="Please enter a valid keycode.")])       

class GameUploadForm(FlaskForm):
    game_rom = FileField('game_rom',validators=[FileSize(4*2**10)])
    title = StringField('Title',
                        validators=[InputRequired(),Length(min=1,max=255),Regexp("^[0-9a-zA-z \.\?\!\,\']+$",message='Only letters, numbers, spaces and the following punctuation are allowed: !?.\',')],
                        filters=[strip_whitespace])
    description = TextAreaField('Description',validators=[InputRequired(),Length(min=1,max=5000)])
    key_codes = FieldList(FormField(KeyConfigForm),min_entries=16,max_entries=16)

