"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

import os
import mlab
from mongoengine import *
from flask import *
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')

#app config là global, gọi ở đâu cũng dc
app.config["IMG_PATH"] = os.path.join( app.root_path,"static", "img")


#1. Connect
mlab.connect()

#2. Add data
class Item(Document):
    image = StringField()
    title = StringField()
    link = StringField()
    describtion = StringField()
#
# item1 = Item( image =  "http://pics.dmm.co.jp/mono/movie/adult/1star606/1star606ps.jpg"
#               ,title = "STAR-606",
#               link = "http://www.javlibrary.com/en/?v=javliir44m",
#               describtion = "Repeat Senna Matsuoka ... Kiss Instinct Bare Thick 4 Sex"
#               )
#
# # item1.save()
#
#
# ###
# # Routing for your application.
# ###
#
#
# items = [
#     {
#         "image": "http://lpjp-dunebuggysrl.netdna-ssl.com/media/catalog/product/LCI/Gb/4L/U6EaumnQPaAuYvkq7-w-i-V09RyV0SkLRlceNaJ7ImRzIjoic21hbGxfaW1hZ2UiLCJmIjoiXC9DXC9GXC9JXC9MXC9QXC9EXC85XC8wXC82XC83XC82XC8wXC9DRklMUEQ5MDY3NjBfTlIwMDAyXzEwMF8xLmpwZyIsImZhIjoxLCJmZiI6MSwiZmgiOjYwMSwiZnEiOjkwLCJmdCI6MSwiZnciOjQxMH0~.jpg"
#         ,"title": "Bodice"
#         ,"price": "1335"
#     },
#
#     {
#         "image":"http://lpjp-dunebuggysrl.netdna-ssl.com/media/catalog/product/LCI/kx/VK/Grj4NVrJjagbdhpfg40LwlAhOtDfjociKGw6ktl7ImRzIjoic21hbGxfaW1hZ2UiLCJmIjoiXC9DXC9GXC9JXC9MXC9QXC9EXC8wXC8wXC8yXC8yXC85XC81XC9DRklMUEQwMDIyOTU1X05SMDAwMl8xMDBfMS5qcGciLCJmYSI6MSwiZmYiOjEsImZoIjo2MDEsImZxIjo5MCwiZnQiOjEsImZ3Ijo0MTB9.jpg"
#         ,"title":"Thong in"
#         ,"price": "234"
#     },
#
#     {
#         "image":"http://lpjp-dunebuggysrl.netdna-ssl.com/media/catalog/product/LCI/Bc/B4/swCYODnJGzU4cfprkDL-ifgzM1NNMNZY832oUV97ImRzIjoic21hbGxfaW1hZ2UiLCJmIjoiXC9DXC9GXC9JXC9MXC9QXC9EXC8wXC8wXC8yXC8yXC85XC81XC9DRklMUEQwMDIyOTUwX05SMDAwMl8xMDAuanBnIiwiZmEiOjEsImZmIjoxLCJmaCI6NjAxLCJmcSI6OTAsImZ0IjoxLCJmdyI6NDEwfQ~~.jpg"
#         ,"title": "Crepe-de-chine"
#         ,"price": "813"
#     }
# ]

@app.route('/index')
def index():
    if "logged_in" not in session:
        flash("You must log in first")
        return redirect( url_for("login"))
    return render_template("index.html", items = Item.objects() )

@app.route("/add-movie", methods = ["GET", "POST"])
def add_lingerie():
    if request.method == "GET" : #Client asking for FORM
        return render_template("add_item.html")
    elif request.method == "POST": #Client submitting FORM
        #1. Get data from FORM (Title, Image, Price)
        form = request.form #input là dictionary => name là key
        title = form["title"]
        link = form["link"]
        describtion = form["describtion"]
        # image = form["image"]

        image = request.files["image"]
        filename = secure_filename(image.filename) # make image name machine-friendly
        save_location = os.path.join( app.config["IMG_PATH"], filename)
        print(save_location)
        image.save(save_location)


        # if not isinstance(describtion, text):
        #     return redirect(url_for("add_lingerie"))


        # 2. Create data (database)
        item = Item (title = title,
                     link = link,
                     describtion = describtion,
                     image = "/images/{0}".format(filename)
                     )
        item.save()

        #3. Redirect

        return redirect(url_for("index"))

@app.route("/login", methods = ["GET", "POST"])
@app.route("/", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        form = request.form
        #1. Retrieve username and password
        username = form['username']
        password = form['password']
        #2. Authenticate
        if username == "admin" and password == "admin":
            session["logged_in"] = True
            return redirect(url_for("index"))
        else:
            # return "Sai pass r, óc chó ạ"
            #Dùng flash message:
            flash("Nhập sai r, óc chó")
            return render_template("login.html")


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

@app.route("/images/<image_name>")
def image(image_name):
    print(app.config["IMG_PATH"])
    return send_from_directory(app.config["IMG_PATH"], image_name )


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    # app.run(debug=True)  => làm sever restart => chạy 2 lần
    app.run( debug= False)
