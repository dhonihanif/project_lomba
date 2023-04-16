from flask import Flask, render_template, request, redirect, session, url_for
from flask_mysqldb import MySQL
from flask_assets import Environment, Bundle
import json, os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
assets = Environment(app)

js = Bundle('chart.js', output='static/assets/js/main.js')
css = Bundle('chart.css', output='static/assets/css/main.css')
assets.register('js_all', js)
assets.register('css_all', css)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "lomba"
app.secret_key='asdsdfsdfs13sdf_df%&'

mysql = MySQL(app)
@app.route("/")
def index():
    global curfet
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM login")
    curfet = cur.fetchall()
    name_user = [i[2] for i in curfet]
    login = False
    if "username" in session:
        login = True
        email = session["username"]
        return render_template("index.html", login=login, username=email, name_user=name_user, user2=session["username"])
    return render_template("index.html", login=login, name_user=name_user)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("email")
        password = request.form.get("password")
        user = [i[0] for i in curfet]
        pw = [i[1] for i in curfet]
        nama = [i[2] for i in curfet]
        name = nama[user.index(username)-1]
        if username in user and password in pw:
            session["username"] = username
            session["password"] = password
            session["nama"] = name
            return redirect(url_for("index"))
        else:
            return render_template("./login/login.html")

    else:
        return render_template("./login/login.html")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("name")
        usia = request.form.get("usia")
        tinggal = request.form.get("tinggal")
        telp = request.form.get("telp")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO login(username, password, name, usia, tempat_tinggal, telp) values (%s, %s, %s, %s, %s, %s)", (username, password, name, usia, tinggal, telp))
        cur2 = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("login"))
    else:
        return render_template("./login/register.html")

@app.route("/forgot_password")
def forgot_password():
    login = False
    user = ""
    if "username" in session:
        login = True
        user = session["username"]
    return render_template("./login/forgot_password.html", username=user)

@app.route("/logout")
def logout():
    session.pop("username",None)
    session.pop("password", None)
    session.pop("nama", None)
    return redirect(url_for('index'))

@app.route("/about")
def about():
    login = False
    user = ""
    if "username" in session:
        login = True
        user = session["username"]
    return render_template("about.html", login=login, username=user)

@app.route("/destination/<name_province>/<name_destination>")
def destination(name_province ,name_destination):
    login = False
    user = ""
    if "username" in session:
        login = True
        user = session["username"]
    cur = mysql.connection.cursor()
    # cur.execute("SELECT * from posting if ")
    # bali = 
    return render_template(f"./destination/{name_province}/{name_destination}.html", login=login, username=user)

@app.route("/contact")
def contact():
    login = False
    user = ""
    if "username" in session:
        login = True
        user = session["username"]
    return render_template("contact.html", login=login, username=user)

@app.route("/profile/<username>")
def profile(username):
    login = False
    user = ""
    if "username" in session:
        login = True
        user = session["nama"]
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM login WHERE username='{username}'")
        member = cur.fetchall()
        email = member[0][0]
        name = member[0][2]
        usia = member[0][4]
        tempat_tinggal = member[0][3]
        no_telp = member[0][5]

    return render_template("profile.html", login=login, user=user, email=email, name=name, 
                           usia=usia, tempat_tinggal=tempat_tinggal, no_telp=no_telp, username=session["username"])

@app.template_global(name='zip')
def _zip(*args, **kwargs): #to not overwrite builtin zip in globals
    return __builtins__.zip(*args, **kwargs)

@app.route("/statistics/<name_destination>")
def statistics(name_destination):
    # data statistik
    tahun = json.load(open("static/assets/json/tahun.json"))
    bali = json.load(open("static/assets/json/bali.json"))
    papua = json.load(open("static/assets/json/raja_ampat.json"))
    yogyakarta = json.load(open("static/assets/json/yogyakarta.json"))
    palembang = json.load(open("static/assets/json/palembang.json"))
    sulawesi = json.load(open("static/assets/json/tana_toraja.json"))
    ntt = json.load(open("static/assets/json/ntt.json"))
    jakarta = json.load(open("static/assets/json/jakarta.json"))

    if name_destination == "bali":
        data = [bali[i] for i in bali if bali[i] != None]
        tahun = [tahun[i] for i in tahun if bali[i] != None]
    elif name_destination == "papua":
        data = [papua[i] for i in papua if papua[i] != None]
        tahun = [tahun[i] for i in tahun if papua[i] != None]
    elif name_destination == "yogyakarta":
        data = [yogyakarta[i] for i in yogyakarta if yogyakarta[i] != None]
        tahun = [tahun[i] for i in tahun if yogyakarta[i] != None]
    elif name_destination == "palembang":
        data = [palembang[i] for i in palembang if palembang[i] != None]
        tahun = [tahun[i] for i in tahun if palembang[i] != None]
    elif name_destination == "sulawesi":
        data = [sulawesi[i] for i in sulawesi if sulawesi[i] != None]
        tahun = [tahun[i] for i in tahun if sulawesi[i] != None]
    elif name_destination == "ntt":
        data = [ntt[i] for i in ntt if ntt[i] != None]
        tahun = [tahun[i] for i in tahun if ntt[i] != None]
    elif name_destination == "jakarta":
        data = [jakarta[i] for i in jakarta if jakarta[i] != None]
        tahun = [tahun[i] for i in tahun if jakarta[i] != None]
    
    df = pd.DataFrame({"tahun": [i for i in tahun], "data": [i for i in data]})
    login = False
    user = ""
    if "username" in session:
        login = True
        user = session["username"]
    return render_template(f"./statistics/{name_destination}.html", tahun=tahun, data=data,
                           min=df["data"].min(), max=df["data"].max(), mean=df["data"].mean(), variance=df["data"].var(), 
                           username=user, login=login)

@app.route("/create_posting", methods=["GET", "POST"])
def create_posting():
    login = True
    user = session["username"]
    if request.method == "POST":
        title = request.form.get("title")
        sub_title = request.form.get("sub_title")
        location = request.form.get("location")
        source = request.form.get("source")
        destination = request.form.get("destination")
        image = request.files["image"]
        image_name = image.filename
        image_path = os.path.join(f"static/assets/img/destination/bali/", image_name)
        image.save(image_path)
        content = request.form.get("content")
        username = session["username"]
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO posting (title, sub_title, image, location, source, destination, content, username) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (title, sub_title, image_path, location, source, destination, content, username))
        cur2 = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        return redirect(url_for(f"destination", name_province=destination, name_destination=destination))
    else:
        return render_template("create_posting.html", login=login, username=user)

@app.route("/food")
def food():
    login = False
    user = ""
    if "username" in session:
        login = True
        user = session["username"]
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM food")
    shop = cur.fetchall()
    
    title = [i[0] for i in shop]
    describe = [i[1] for i in shop]
    image = [i[2] for i in shop]
    price = [i[3] for i in shop]
    destination = [i[4] for i in shop]
    return render_template(f"./food/shop.html", login=login, username=user, title=title, describe=describe, image=image,
                           price=price, destination=destination)

@app.route("/food/<name_province>/<name_destination>")
def foodd(name_province, name_destination):
    login = False
    user = ""
    if "username" in session:
        login = True
        user = session["username"]
    
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM food WHERE title LIKE '%{name_destination}%' AND destination = '{name_province}'")
    shop = cur.fetchall()
    
    title = shop[0][0]
    describe = shop[0][1]
    image = shop[0][2]
    price = shop[0][3]
    destination = shop[0][4]
    stock = shop[0][5]

    return render_template(f"./food/{name_province}/{name_destination}.html", login=login, username=user,
                           title=title, describe=describe, image=image, price=price,
                           destination=destination, stock=stock)

@app.route("/cart")
def cart():
    login = False
    user = ""
    
if __name__ == "__main__":
    app.run(debug=True)