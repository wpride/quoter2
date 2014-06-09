from flask import Flask
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

@app.route('/')
def hello():
	return "Hello Derpy World!"

@app.route('/<name>')
def hello_name(name):
	return "Hello {} you derp!".format(name)

if __name__ == '__main__':
	print os.environ['APP_SETTINGS']
	app.run()
