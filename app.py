from flask import Flask, render_template, flash, redirect
import redis
from collections import defaultdict
import os
from forms import LoginForm

app = Flask(__name__)
app.debug = True
app.config.from_object('config')
redis_url = os.getenv('REDISTOGO_URL', 'localhost')
r_server = redis.from_url(redis_url)

@app.route('/')
def hello2():

    mclips = r_server.keys()

    accumulator = ""

    for elem in mclips:

        accumulator = accumulator + "{" + elem + " } "

    return render_template('base.html') + accumulator

@app.route('/index')
def hello():
    return render_template('base.html') + "Ned is Gay.com"

@app.route('/tag', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for tag= ' + form.tagid.data + ' clip= ' + form.clipid.data)

        index = form.clipid.data.index("v=")+2
        newClipId = form.clipid.data[index:]
        splitstring = form.tagid.data.replace(' ',',').split(',')
        for elem in splitstring:
            elem.strip()
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