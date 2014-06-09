from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import redis
from collections import defaultdict
import operator
import os

app = Flask(__name__)
redis_url = os.getenv('REDISTOGO_URL', 'localhost')
r_server = redis.Redis('localhost')

@app.route('/')
def hello():
    return "Hello Derpy Herpy World!"

@app.route('/<name>')
def hello_name(name):

    splitstring = name.split('_')
    accumulator = ""
    countmap=defaultdict(int)

    for splitsegment in splitstring:
        mclips = r_server.sinter(splitsegment)
        accumulator += splitsegment
        for elem in mclips:
            countmap[elem] += 1

    result = max(countmap.iteritems(), key=lambda x: x[1])

    return "<a href='https://www.youtube.com/watch?v={}'>Clip</a>".format(result[0])

if __name__ == '__main__':
	app.run()
