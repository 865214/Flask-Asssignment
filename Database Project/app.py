from flask import Flask, render_template, request, redirect, url_for, get_flashed_messages
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    age = db.Column(db.Integer)

    def __repr__(self):
        return f'The user {self.name} is {self.age} years old'

class AddUserForm(FlaskForm):
    name = StringField('Name of the user')
    age = IntegerField('Age of the user')
    submit = SubmitField('Submit')

class DeleteUserForm(FlaskForm):
    name = StringField('Name of the user')
    age = IntegerField('Age of the user')
    submit = SubmitField('Submit')

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/addusers', methods=['GET', 'POST'])
def add_users():
    form = AddUserForm()

    if form.validate_on_submit():
        name = form.name.data
        age = form.age.data
        user = User(name=name, age=age)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        return redirect(url_for('list_users'))
    return render_template('add.html', form=form)

@app.route('/delete', methods=['GET', 'POST'])
def delete_user():
    form = DeleteUserForm()

    if form.validate_on_submit():
        name = form.name.data
        age = form.age.data
        user_to_delete = User.query.filter_by(name=name, age=age).first()
        try:
            db.session.delete(user_to_delete)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        return redirect(url_for('list_users'))
    return render_template('delete.html', form=form)

@app.route('/list')
def list_users():
    users = User.query.all()
    return render_template('list.html', users=users)

if __name__ == '__main__':
    app.run()