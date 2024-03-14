from flask import Flask, render_template, url_for, request, redirect
from flask_bootstrap import Bootstrap4
from forms import UploadProject
from flask_ckeditor import CKEditorField, CKEditor
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Text, Column, text

# Create applications to run
app = Flask('__main__')
Bootstrap4(app)
ckeditor = CKEditor(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Projects.db'
app.config['SECRET_KEY'] = 'Yourmom'

# Initialize DATABASE
db = SQLAlchemy(app)


# CREATE Database for uploaded projects
class ProjectPost(db.Model):
    id = db.Column(Integer, primary_key=True)
    title = db.Column(String, unique=False, nullable=True)
    subtitle = db.Column(String, unique=False, nullable=True)
    img_url = db.Column(String, nullable=False)
    body = db.Column(String, nullable=False)
    techniques_applied = db.Column(db.String, nullable=False)



with app.app_context():
    all_p = ProjectPost.query.all()
    for post in all_p:
        if post.id == 0:
            db.session.delete(post)
            db.session.commit()
        print(post.id)


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(ProjectPost))
    projects = result.scalars().all()
    return render_template("home.html", all_posts=projects)


@app.route('/post/<post_id>')
def show_post(post_id):
    requested_post = db.get_or_404(ProjectPost, post_id)
    return render_template('post.html', post=requested_post)


@app.route('/Project', methods=['POST', 'GET'])
def show_project():
    form = UploadProject()
    if form.validate_on_submit():
        with app.app_context():
            new_post = ProjectPost(
                title= form.data['title'],
                subtitle= form.data['subtitle'],
                img_url= form.data['img_url'],
                body= form.data['body'],
                techniques_applied=form.data['techniques_applied'],
            )
            db.session.add(new_post)
            db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template('addproject.html', form=form)

@app.route('/post/<post_id>/edit',methods=['POST','GET'])
def edit_post(post_id):
    requested_post = db.get_or_404(ProjectPost, post_id)
    edit_form = UploadProject(
        title=requested_post.title,
        subtitle=requested_post.subtitle,
        img_url=requested_post.img_url,
        body=requested_post.body,
        techniques_applied=requested_post.techniques_applied,
    )

    if edit_form.validate_on_submit():
        requested_post.title = edit_form.data['title']
        requested_post.subtitle = edit_form.data['subtitle']
        requested_post.img_url = edit_form.data['img_url']
        requested_post.body = edit_form.data['body']
        requested_post.techniques_applied = edit_form.data['techniques_applied']
        db.session.commit()
        return redirect(url_for("show_post", post_id=post_id))
    return render_template('addproject.html', form=edit_form, is_edit=True)


@app.route('/post/<post_id>/delete')
def delete(post_id):
    post_to_delete = db.get_or_404(ProjectPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))



if __name__ == '__main__':
    app.run(debug=True)
