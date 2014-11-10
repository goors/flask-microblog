from flask import Blueprint, render_template, session, redirect, url_for, request, json
from PostModel import  *
from TagModel import  *
from UserModel import  *

admin_api = Blueprint('admin_api', __name__)


@admin_api.route('/admin', methods=['GET'])
def posts():

    if (session):

        post = PostModel()
        allPosts = post.posts()

        if(allPosts):
            return render_template('admin/index.html', data=session["auth"], posts=allPosts)
        return render_template('admin/index.html', data=session["auth"])

    return redirect("/admin/login")

@admin_api.route('/admin/add-post', methods=['POST','GET'])
def addpost():

    if (session):

        tags = TagModel()
        if request.method == "POST":
            active = 1 if request.form.get('active') else 0
            post = PostModel()
            pid = post.addPost(request.form['title'], request.form['slug'], request.form['content'], request.files['photo'], active)
            post.addTags(request.form.getlist('tags'), pid);

        if (tags.tags()):
            return render_template('admin/add-post.html', data=session["auth"], tags=tags.tags())
        return render_template('admin/add-post.html', data=session["auth"])

    return redirect("/admin/login")

@admin_api.route('/admin/edit-post/<id>', methods=['POST','GET'])

def editpost(id=None):

    if (session):

        post = PostModel()

        tags = TagModel()

        if request.method == "POST":


            active = '1' if request.form.get('active') else '0'
            print active
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


            post.addTags(request.form.getlist('tags'), id);
        single = post.getPost(id)
        postTags = post.getPostTags(id);

        return render_template('admin/add-post.html', data=session["auth"], post=single, tags=tags.tags(), postTags=postTags)
    return redirect("/admin/login")

@admin_api.route('/admin/add-tag', methods=['POST'])
def addtag():

    if (session):
        if request.method == "POST":

            if request.json['name']:
                tags = TagModel()
                id = tags.addtag(request.json['name'])
                response = {'response': request.json['name'], 'status': 1, 'message': "Tag created", 'Id':id}
                print response
            return json.jsonify(response)

    #return redirect("/admin/login")
@admin_api.route('/admin/delete-post/<id>', methods=['GET'])
def deletepost(id=None):

    if (session):
        post = PostModel()
        post.deletePost(id)

    return redirect("/admin/login")


@admin_api.route('/admin/users', methods=['GET'])
def users():

    if(session):
        user = UserModel();
        return render_template("admin/users.html", users=user.list(), data=session['auth'])
    return redirect("/admin/login")

@admin_api.route('/admin/edit-user/<id>', methods=['GET','POST'])
def edituser(id = None):

    if(session):
        user = UserModel()

        if request.method == "POST":
            user.register(request.form['email'], request.form['password'], request.form['nick'], request.form['role'], id)

        return render_template("admin/add-user.html", data=session['auth'], user=user.getUser(id))
    return redirect("/admin/login")

@admin_api.route('/admin/register', methods=['GET','POST'])
def adduser():

    if(session):
        user = UserModel()

        if request.method == "POST":
            user.register(request.form['email'], request.form['password'], request.form['nick'], request.form['role'])

        return render_template("admin/add-user.html", data=session['auth'])
    return redirect("/admin/login")



