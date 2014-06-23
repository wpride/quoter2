from flask import Flask
import redis
from collections import defaultdict
import os

app = Flask(__name__)
app.debug = True
app.config.from_object('config')
redis_url = os.getenv('REDISTOGO_URL', 'localhost')
r_server = redis.from_url(redis_url)

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

if __name__ == '__main__':
	app.run()
