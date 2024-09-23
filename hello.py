from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT Email address?', 
                    validators=[DataRequired(message="Email is required"), 
                                Email(message="Please include an '@' in your email address.")])

    submit = SubmitField('Submit')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')
        
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')
        
        session['name'] = form.name.data
        session['email'] = form.email.data
        
        if 'utoronto' in form.email.data.lower():
            session['is_uoft'] = True
        else:
            session['is_uoft'] = False
            #flash('Please use a UofT email address.')
        
        
        return redirect(url_for('index'))
    
    return render_template('index.html', 
                           form=form, 
                           name=session.get('name'), 
                           email=session.get('email'), 
                           is_uoft=session.get('is_uoft'))
