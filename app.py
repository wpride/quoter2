from flask import Flask, render_template, redirect
from flask.ext.sqlalchemy import SQLAlchemy
import redis
from collections import defaultdict
import operator
import os
from forms import TagForm

app = Flask(__name__)
app.debug = True
app.config.from_object('config')
redis_url = os.getenv('REDISTOGO_URL', 'localhost')
r_server = redis.Redis('localhost')

@app.route('/')
def hello():
    return "Hello Derpy Scurpy World!"

@app.route('/<name>')
def hello_name(name):

    splitstring = name.split('_')
    countmap=defaultdict(int)

    for splitsegment in splitstring:
        mclips = r_server.sinter("tag:"+ splitsegment)
        for elem in mclips:
            countmap[elem] += 1
    try:
        result = max(countmap.iteritems(), key=lambda x: x[1])
    except:
        return "No matches found."

    return "<a href='https://www.youtube.com/watch?v={}'>Clip</a>".format(result[0])

@app.route('/tag', methods = ['GET', 'POST'])
def login():
    form = TagForm()
    return render_template('login.html',
        title = 'Tag',
        form = form)

if __name__ == '__main__':
	app.run()
