from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class TagForm(Form):
    tagid = TextField('tag', validators = [Required()])
    clipid = TextField('clip', validators = [Required()])