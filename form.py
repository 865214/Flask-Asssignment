from flask import Flask, request, render_template, jsonify

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('username.html')

@app.route('/printname', methods = ['POST'])
def printname():
    name = request.form.get('name')
    return f'Your name is {name}'
if __name__ == '__main__':
    app.run()