from flask import Flask, render_template, abort

app = Flask(__name__)

# Define routes
@app.route('/')
def home():
    return 'Hello, this is the home page!'

@app.route('/error_404')
def error_404():
    # Force a 404 error
    abort(404)

@app.route('/error_500')
def error_500():
    raise Exception("This is a simulated internal server error.") 

# Custom error handlers
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error_code=404, error_message="Page not found"), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', error_code=500, error_message="Internal Server Error"), 500

if __name__ == '__main__':
    app.run(debug=True)