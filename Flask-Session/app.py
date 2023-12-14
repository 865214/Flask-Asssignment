from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key for security

# Dummy data for demonstration purposes
users_data = {
    'user1': {'username': 'user1', 'email': 'user1@example.com'},
    'user2': {'username': 'user2', 'email': 'user2@example.com'}
}

@app.route('/')
def home():
    # Check if the user is logged in
    if 'username' in session:
        username = session['username']
        user_data = users_data.get(username, {})
        return render_template('index.html', username=username, user_data=user_data)
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        if username in users_data:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username')
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Clear the session data for the user
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)