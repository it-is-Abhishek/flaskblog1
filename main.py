from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__)

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL='True',
    MAIL_USERNAME=params['gmail_user'],
    MAIL_PASSWORD=params['gmail_password']

)

mail = Mail(app)

if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)


class Contact(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone_no = db.Column(db.String(13), nullable=False)
    mes = db.Column(db.String(120), nullable=False)


class Posts(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    tagline = db.Column(db.String(500), nullable=False)  
    date = db.Column(db.String(15), nullable=True)
    img_name = db.Column(db.String(50), nullable=True)


@app.route('/')
def home():
    posts = Posts.query.filter_by().all()
    return render_template('index.html', params=params, posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', params=params)

@app.route('/dashboard')
def dashboard():
    return render_template('login.html', params=params)

@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=params, post=post)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if (request.method == 'POST'):
        """Add entry to the database"""
        name = request.form.get('name')
        email = request.form.get('phone')
        phone = request.form.get('email')
        message = request.form.get('message')
        entry = Contact(name=name, phone_no=phone, email=email, mes=message)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New Message from ' + name,
                          sender=email,
                          recipients=[params['gmail_user']],
                          body=message + "\n" + phone)

    return render_template('contact.html', params=params)


app.run(debug=True)
