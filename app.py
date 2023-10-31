from flask import Flask
from flask import request
from flask import render_template
from flask import redirect, url_for,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.sqlite"
db.init_app(app)
migrate = Migrate(app, db)
UPLOAD_FOLDER = 'static/iti/images'

app.config['UPLOAD_FOLDER'] = 'media'
UPLOAD_FOLDER = 'static/iti/images' 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/hello')
def hello_world():
    return "<p>Hello, World!</p>"


def user(user):
    return f"<p>heelo{user}</p>"


student=[
    {"id":1,"name":"mina","age":10},
    {"id": 2, "name": "wael", "age": 10}
]
# @app.route('/users')
# def list():
#     return student
@app.route('/post/<int:id>', endpoint="view")
def view(id):
    post=Post.selected_post(id)
    return render_template('view.html',post=post)

class Post(db.Model):
    __tablename__="info"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.String)
    image = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    @classmethod
    def get_all_post(cls):
        return cls.query.all()
    @classmethod
    def selected_post(cls,id):
        return cls.query.get_or_404(id)
    @classmethod
    def delete_post(cls,id):
        post= cls.query.get_or_404(id)
        db.session.delete(post)
        db.session.commit()
    @property
    def url_delete(self):
        return (url_for("delete",id=self.id))  
    @property
    def url_show(self):
        return (url_for("view",id=self.id))  
    @classmethod
    def save_post(cls,requestdata):
        post= cls(**requestdata)
        db.session.add(post)
        db.session.commit() 
        return post
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in set(['jpg', 'jpeg', 'png', 'gif'])

@app.route("/" ,endpoint="post")
def posts():
    posts=Post.query.all()
    return render_template("index.html",post=posts)

@app.route('/aboutus', endpoint="about")
def aboutus():
     return render_template("aboutus.html")
@app.route('/contactus', endpoint="contact")
def aboutus():
     return render_template("contactus.html")


@app.route('/post/<int:id>/delete', endpoint="delete")
def delete(id):
    post=Post.delete_post(id)
    return redirect(url_for("post"))
@app.route('/create', endpoint="create",methods=['POST','GET'])
def create():
 if request.method == 'POST':

        image = request.files['image']

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
        else:
            filename = None

        post = Post(title=request.form['title'], body=request.form['body'], image=filename)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('post'))

 return render_template('create.html')

@app.route('/update/<int:id>', endpoint="update",methods=['POST','GET'])  
def update(id):

 post = Post.query.get_or_404(id)

 if request.method == 'POST':

        post.title = request.form['title']
        post.body = request.form['body']

        new_image = request.files['image']
        if new_image and allowed_file(new_image.filename):
            filename = secure_filename(new_image.filename)
            new_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            post.image = filename

        db.session.commit()
        return redirect(url_for('post', id=post.id))

 return render_template('update.html', post=post)




       
if __name__=='__main__':
    app.run(debug=True)