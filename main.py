from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG']  = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog00:buildablog00@localhost:8889/build-a-blog00'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1024))

    def __init__(self, title, body):
        self.title = title       
        self.body = body

@app.route('/')
def index():   
    return redirect('/blog')


@app.route('/blog', methods=['GET'])
def blog():
    blog_id = request.args.get('id')
    blogs = Blog.query.all()    
    if blog_id:
        blog = Blog.query.get(blog_id)
        blog_title = blog.title
        blog_body = blog.body
        return  render_template('entry.html', blog_title=blog_title, blog_body=blog_body)
    else: 
        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']   
        title_error =''
        body_error = ''
        if len(blog_title) == 0:
            title_error = "Please fill in the blog title."
        if len(blog_body) == 0:
            body_error = "Please fill in the blog body."
        if not title_error and not body_error:
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
        
            
            return redirect('/blog?id={0}'.format(new_blog.id)) 
        else:
            return render_template('newpost.html',  blog_title = blog_title, title_error = title_error, blog_body = blog_body,  body_error = body_error)
    else:
        return render_template('newpost.html')
if __name__ == "__main__":
    app.run()

