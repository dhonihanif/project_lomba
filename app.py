from flask import Flask, render_template, request, redirect, session, url_for
from flask_mysqldb import MySQL
from flask_assets import Environment, Bundle
import os, html, json

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
    user = [i[2] for i in curfet]
    login = False
    if "username" in session:
        login = True
        return render_template("index.html", login=login, user=user, user2=session["username"])
    return render_template("index.html", login=login, user=user)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("name")
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
            return render_template("login.html")

    else:
        return render_template("login.html")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
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
        return render_template("register.html")

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
    return render_template("about.html", login=login, user=user)

@app.route("/destination/<name_province>/<name_destination>")
def destination(name_province ,name_destination):
    login = False
    user = ""
    if "username" in session:
        login = True
        user = session["username"]
    return render_template(f"./destination/{name_province}/{name_destination}.html", login=login, user=user)

@app.route("/contact")
def contact():
    login = False
    user = ""
    if "username" in session:
        login = True
        user = session["username"]
    return render_template("contact.html", login=login, user=user)

@app.route("/statistics/<name_destination>")
def statistics(name_destination):
    # data statistik
    tahun = json.load(open("static/assets/json/tahun.json"))
    bali = json.load(open("static/assets/json/bali.json"))
    raja_ampat = json.load(open("static/assets/json/raja_ampat.json"))
    yogyakarta = json.load(open("static/assets/json/yogyakarta.json"))
    palembang = json.load(open("static/assets/json/palembang.json"))
    tana_toraja = json.load(open("static/assets/json/tana_toraja.json"))
    lombok = json.load(open("static/assets/json/lombok.json"))
    ntt = json.load(open("static/assets/json/ntt.json"))

    data_tahun = [tahun[i] for i in tahun]
    if name_destination == "bali":
        data = [bali[i] for i in bali]
    elif name_destination == "raja_ampat":
        data = [raja_ampat[i] for i in raja_ampat]
    elif name_destination == "yogyakarta":
        data = [yogyakarta[i] for i in yogyakarta]
    elif name_destination == "palembang":
        data = [palembang[i] for i in palembang]
    elif name_destination == "tana_toraja":
        data = [tana_toraja[i] for i in tana_toraja]
    elif name_destination == "lombok":
        data = [lombok[i] for i in lombok]
    elif name_destination == "ntt":
        data = [ntt[i] for i in ntt]
    
    return render_template(f"./statistics/{name_destination}.html", tahun=data_tahun, data=data)

if __name__ == "__main__":
    app.run(debug=True)