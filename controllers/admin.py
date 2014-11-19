from flask import Blueprint, render_template, session, redirect, url_for, request, json, flash
from PostModel import  *
from TagModel import  *
from UserModel import  *

admin_api = Blueprint('admin_api', __name__)

@admin_api.before_request
def before_request():
    if 'Id' not in session and request.endpoint != '/admin/login':
        return redirect("/admin/login")

@admin_api.route('/admin', methods=['GET'])
def posts():

    post = PostModel()
    allPosts = post.posts()

    if(allPosts):
        return render_template('admin/index.html', posts=allPosts)
    return render_template('admin/index.html')


@admin_api.route('/admin/add-post', methods=['POST','GET'])
def addpost():


    tags = TagModel()
    if request.method == "POST":
        active = 1 if request.form.get('active') else 0
        post = PostModel()
        pid = post.addPost(request.form['title'], request.form['slug'], request.form['content'], request.files['photo'], active)
        post.addTags(request.form.getlist('tags'), pid);

        if(request.files["files"]):
            post.addFiles(request.files.getlist("files"), pid)

        if(request.files["images"]):
            post.addImages(request.files.getlist("images"), pid)
        return redirect("/admin/edit-post/"+str(pid))
    return render_template("admin/add-post.html", tags=tags.tags())


@admin_api.route('/admin/edit-post/<id>', methods=['POST','GET'])
def editpost(id=None):

    post = PostModel()

    tags = TagModel()

    if request.method == "POST":


        active = '1' if request.form.get('active') else '0'
        if request.files['photo']:

            file = request.files['photo']

        else:
            file = False

        post.addPost(
            request.form['title'],
            request.form['slug'],
            request.form['content'],
            file,
            active,
            id)

        post.addTags(request.form.getlist('tags'), id)

        if request.files["files"]:
            post.addFiles(request.files.getlist("files"), id)
        if request.files["images"]:
            post.addImages(request.files.getlist("images"), id)
        flash('You have successfully update post.')

    single = post.getPost(id)
    postTags = post.getPostTags(id)
    postFiles = post.getPostFiles(id)
    postImages = post.getPostImages(id)

    return render_template('admin/add-post.html', post=single, tags=tags.tags(), postTags=postTags, postFiles=postFiles, postImages=postImages)

@admin_api.route('/admin/add-tag', methods=['POST'])
def addtag():
    if request.method == "POST":

        if request.json['name']:
            tags = TagModel()
            id = tags.addtag(request.json['name'])
            response = {'response': request.json['name'], 'status': 1, 'message': "Tag created", 'Id': id}
            print response
        return json.jsonify(response)

@admin_api.route('/admin/delete-file', methods=['POST'])
def deletefile():
    if request.method == "POST":

        if request.json['id']:
            post = PostModel()
            post.removefile(request.json['id'])
            response = {'status': 1, 'message': "Deleted"}

        return json.jsonify(response)

@admin_api.route('/admin/delete-image', methods=['POST'])
def deleteimage():
    if request.method == "POST":

        if request.json['id']:
            post = PostModel()
            post.removeimage(request.json['id'])
            response = {'status': 1, 'message': "Deleted"}

        return json.jsonify(response)


@admin_api.route('/admin/delete-post/<id>', methods=['GET'])
def deletepost(id=None):
    post = PostModel()
    post.deletePost(id)
    return redirect("/admin")


@admin_api.route('/admin/users', methods=['GET'])
def users():
    user = UserModel();
    return render_template("admin/users.html", users=user.list())

@admin_api.route('/admin/edit-user/<id>', methods=['GET','POST'])
def edituser(id = None):
    user = UserModel()

    if request.method == "POST":
        user.register(request.form['email'], request.form['password'], request.form['nick'], request.form['role'], id)
        flash('You have successfully update user.')
    return render_template("admin/add-user.html", user=user.getUser(id))

@admin_api.route('/admin/register', methods=['GET','POST'])
def adduser():
    user = UserModel()

    if request.method == "POST":
        u = user.register(request.form['email'], request.form['password'], request.form['nick'], request.form['role'])
    return redirect("/admin/edit-user/"+u)

@admin_api.context_processor
def utility_processor():
    def getNumberOfComments(id):
        p = PostModel()
        return p.getNumberOfComments(id)
    return dict(getNumberOfComments=getNumberOfComments)

