from flask import Flask, request, redirect
import cgi
import os
import re
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    template = jinja_env.get_template('index.html')
    return template.render()

@app.route("/", methods=['POST'])
def submit():
    username = request.form['username']
    username_error = ''
    password = request.form['password']
    password_error = ''
    verify = request.form['verify']
    verify_error = ''
    email = request.form['email']
    email_error = ''

    if not username:
        username_error = "Username is required"
    elif len(re.findall('\S+', username)) != 1 or ' ' in username or len(username) < 3 or len(username) > 20:
        username_error = "Username is not valid"

    if not password:
        password_error = "Password is required"
    elif len(re.findall('\S+', password)) != 1 or ' ' in password or len(password) < 3 or len(password) > 20:
        password_error = "Password is not valid"

    if not verify:
        verify_error = "Verify Password is required"
    elif password != verify:
        verify_error = "Passwords must match"

    if email:
        validated_email = re.findall('\S+@\S+\.\S+', email)
        if len(validated_email) != 1 or len(email) < 3 or len(email) > 20:
            email_error = "Email is not valid"

    password = ''
    verify = ''

    if username_error or password_error or verify_error or email_error:
        template = jinja_env.get_template('index.html')
        return template.render(username=username, username_error=username_error, 
            password=password, password_error=password_error,
            verify=verify, verify_error=verify_error,
            email=email, email_error=email_error)
    else:
        template = jinja_env.get_template('welcome.html')
        return template.render(username=username)

app.run()
