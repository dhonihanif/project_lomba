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
        cur.execute("SELECT count(*) from cart")
        count = cur.fetchall()[0][0]
        return render_template("index.html", login=login, username=email, name_user=name_user, user2=session["username"], count=count)
    return render_template("index.html", login=login, name_user=name_user)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("email")
        password = request.form.get("password")
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM login")
        curfet = cur.fetchall()
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

@app.route("/update_profile/<username>")
def update_profile(username):
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

    return render_template("update_profile.html", login=login, user=user, email=email, name=name, 
                           usia=usia, tempat_tinggal=tempat_tinggal, no_telp=no_telp, username=session["username"])

@app.route("/update", methods=['GET', 'POST'])
def update():
    login = False
    user = ""
    if "username" in session:
        login = True
        user = session["nama"]
        name = request.form.get("name")
        usia = request.form.get("age")
        tempat_tinggal = request.form.get("tinggal")
        no_telp = request.form.get("no_telp")
        cur = mysql.connection.cursor()
        listt = ["name", "tempat_tinggal", "usia", "telp"]
        listt2 = [name, tempat_tinggal, usia, no_telp]
        for i, j in zip(listt, listt2):
            username = session["username"]
            cur.execute(f"UPDATE login SET {i} = '{j}' WHERE username='{username}'")
            mysql.connection.commit()
        
        cur.close()
    
    return redirect(url_for("profile", username=username))

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

@app.route("/return_cart")
def return_cart():
    login = False
    user = ""
    if "username" in session:
        login = True
        user = session["username"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM cart")
        curfet = cur.fetchall()
        images = [i[2] for i in curfet]
        title = [i[1] for i in curfet]
        price = [i[3] for i in curfet]
        purchase_amount = [i[4] for i in curfet]

        return render_template("cart.html", login=login, username=user,
                           images=images, title=title, price=price, purchase_amount=purchase_amount, total=sum(price))
    return redirect(url_for("login"))

@app.route("/cart", methods=["GET","POST"])
def cart():
    login = False
    user = ""
    if "username" in session:
        login = True
        user = session["username"]
        data = request.get_json()
        cur = mysql.connection.cursor()
        query = "INSERT INTO cart (title, images, price, purchase_amount, username) values (%s, %s, %s, %s, %s)"
        cur.execute(query, (data["title"], data["image"], data["price"], data["purchase_amount"], user))
                    
        cur.fetchall()
        mysql.connection.commit()
        cur.close()
        
        redirect(url_for("return_cart"))

    return redirect(url_for("login"))     

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    login = False
    user = ""
    if "username" in session:
        login = True
        user = session["username"]
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT title, price, purchase_amount, if(purchase_amount>0, price*purchase_amount, 0) as sum FROM cart WHERE username='{user}'")
        cart = cur.fetchall()
        global title
        title = [i[0] for i in cart]
        price = [i[1] for i in cart]
        purchase = [i[2] for i in cart]
        total = [i[3] for i in cart]

    return render_template("checkout.html", login=login, username=user,
                           title=title, price=price, purchase=purchase, sub_total=total, total=sum(total))

@app.route("/remove/<title>")
def remove(title):
    cur = mysql.connection.cursor()
    cur.execute(f"DELETE FROM cart WHERE title='{title}'")
    cur.fetchall()
    mysql.connection.commit()
    cur.close()
    
    return redirect(url_for("return_cart"))

@app.route("/order", methods=["GET", "POST"])
def pesan():
    login = False
    if "username" in session:
        login = True
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM cart WHERE username='{session['username']}'")
    curfet = cur.fetchall()
    user = [i[1] for i in curfet if i[1] == session["username"]]
    if request.method == "POST":
        food = ",".join(title)
        payment = request.form.get("pembayaran")
        price = request.form.get("total")
        bayar = "Already Paid"
        cur.execute("INSERT INTO pesanan(food, payment, price, bayar, username) values ('%s', '%s', '%s', '%s', '%s')" % (food, payment, price, bayar, session["username"]))
        cur2 = cur.fetchall()
        mysql.connection.commit()
        cur.execute("DELETE FROM cart WHERE username='%s'" % (session["username"]))        
        cur.fetchall()
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("pesanan", login=login, user=user, username=user))
    else:
        return render_template("pesan.html", login=login, user=user, username=user)

@app.route("/pesanan")
def pesanan():
    login = False
    if "username" in session:
        login = True
    return redirect(url_for("index"))

@app.route("/food_admin")
def food_admin():
    login = False
    user = ""
    if "username" in session:
        login = True
        user = session["username"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT username, food, diantar from pesanan WHERE bayar != 'Not yet paid'")
        cur2 = cur.fetchall()
        usernames = [i[0] for i in cur2]
        food = [i[1] for i in cur2]
        diantar = [i[2] for i in cur2]
        total = len(usernames)
        length = [i+1 for i in range(total)]
    
    return render_template("food_admin.html", login=login, username=user, data=usernames, length=length, total=total, food=food, diantar=diantar)

@app.route("/button_food/<username>")
def button_food(username):
    cur = mysql.connection.cursor()
    cur.execute(f"DELETE FROM pesanan WHERE username='{username}'")
    cur.fetchall()
    mysql.connection.commit()
    cur.close()
    
    return redirect("food_admin")

@app.route("/member")
def member():
    login = False
    user = ""
    if "username" in session:
        login = True
        user = session["username"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM LOGIN")
        cur2 = cur.fetchall()
        usernames = [i[0] for i in cur2][1:]
        total = len(usernames)
        length = [i+1 for i in range(total)]

    return render_template("member.html", login=login, username=user, data=usernames, length=length, total=total)

@app.route("/button_member/<username>")
def button_member(username):
    cur = mysql.connection.cursor()
    cur.execute(f"DELETE FROM login WHERE username='{username}'")
    cur.fetchall()
    mysql.connection.commit()
    cur.close()
    
    return redirect("member")

if __name__ == "__main__":
    app.run(debug=True)