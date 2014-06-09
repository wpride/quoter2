from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import redis
from collections import defaultdict
import operator

app = Flask(__name__)
r_server = redis.Redis('localhost')

@app.route('/')
def hello():
    return "Hello Derpy World!"

@app.route('/<name>')
def hello_name(name):

    splitstring = name.split('_')
    accumulator = ""
    countmap=defaultdict(int)

    for splitsegment in splitstring:
        mclips = r_server.sinter("tag:"+splitsegment)
        accumulator += splitsegment
        for elem in mclips:
            countmap[elem] += 1

    result = max(countmap.iteritems(), key=lambda x: x[1])

    clip_key = result[0]

    clip_path = r_server.get("clip:"+clip_key)

    return "<a href='https://www.youtube.com/watch?v={}'>Clip</a>".format(clip_path)

if __name__ == '__main__':
	app.run()
