from flask import Flask, render_template, flash, redirect
import redis
from collections import defaultdict
import os
from forms import LoginForm
from flask.ext.mongoengine import MongoEngine
from flask.ext.security import Security, MongoEngineUserDatastore, \
    UserMixin, RoleMixin, login_required

app = Flask(__name__)
app.debug = True
app.config.from_object('config')
redis_url = os.getenv('REDISTOGO_URL', 'localhost')
r_server = redis.from_url(redis_url)

# MongoDB Config
app.config['MONGODB_DB'] = 'default'
app.config['MONGODB_HOST'] = 'localhost'
app.config['MONGODB_PORT'] = 27017

# Create database connection object
db = MongoEngine(app)

class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

class User(db.Document, UserMixin):
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])

# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create a user to test with
@app.before_first_request
def create_user():
    user_datastore.create_user(email='wsp260@dimagi.com', password='password')

@app.route('/')
@login_required
def hello2():

    mclips = r_server.keys()

    accumulator = ""

    for elem in mclips:

        accumulator = accumulator + "{" + elem + " } "

    return render_template('base.html') + accumulator

@app.route('/index')
def hello():
    return render_template('base.html') + "Neddard is Gay.com"

@app.route('/tag', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for tag= ' + form.tagid.data + ' clip= ' + form.clipid.data)

        index = form.clipid.data.index("v=")+2
        if(index > 0):
            newClipId = form.clipid.data[index:]
        else:
            newClipId = form.clipid.data
        splitstring = form.tagid.data.replace(' ',',').split(',')
        for elem in splitstring:
            elem = elem.strip()
            elem = elem.lower()
            r_server.sadd("tag:"+elem , newClipId)
        return redirect('/')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/r/<name>')
def hello_name(name):

    splitstring = name.split('_')
    countmap=defaultdict(int)

    accumulator = ""

    for splitsegment in splitstring:
        mclips = r_server.sinter("tag:"+ splitsegment)
        for elem in mclips:
            countmap[elem] += 1
            accumulator = accumulator + "<a href='https://www.youtube.com/watch?v={}'>Clip</a>".format(elem) + "<br/>"
    try:
        result = max(countmap.iteritems(), key=lambda x: x[1])
    except:
        return "No matches found."

    #return "<a href='https://www.youtube.com/watch?v={}'>Clip</a>".format(result[0])
    return accumulator

if __name__ == '__main__':
    app.run()