from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello world'

@app.route('/next')
def next():
    subprocess.Popen("python ../mechanical_trigger.py next", shell=True)
    return "Receive next page"

@app.route('/last')
def last():
    subprocess.Popen("python ../mechanical_trigger.py prev", shell=True)
    return "Receive last page"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
