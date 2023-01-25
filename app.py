from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import datetime
import collections
import json

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://ming:20020622@127.0.0.1:5432/movie"
db = SQLAlchemy(app)
login = False
uid, name, mail, phone, birth, level = 0, "", "", "", "", ""
points, order_numbering = 0, None
record = ()

class users(db.Model):
    uid = db.Column(db.Integer, primary_key = True)
    idcard = db.Column(db.TEXT, unique = True, nullable = False)
    name = db.Column(db.TEXT, unique = False, nullable = False)
    birth = db.Column(db.TEXT, unique = False, nullable = False)
    phone = db.Column(db.TEXT, unique = True, nullable = False)
    mail = db.Column(db.TEXT, unique = True, nullable = False)
    password = db.Column(db.TEXT, unique = False, nullable = False)
    points = db.Column(db.Integer, unique = False, nullable = False)
    level = db.Column(db.TEXT, unique = False, nullable = False)
    
    def __init__(self, idcard, name, birth, phone, mail, password):
        self.idcard = idcard
        self.name = name
        self.birth = birth
        self.phone = phone
        self.mail = mail
        self.password = password
        self.points = 0
        self.level = "一般會員"

class orders(db.Model):
    numbering = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, unique = False, nullable = False)
    session_id = db.Column(db.Integer, unique = False, nullable = False)
    reserve_date = db.Column(db.Date, unique = False, nullable = False)
    get_ticket = db.Column(db.Boolean, unique = False, nullable = False)
    seat = db.Column(db.TEXT, unique = False, nullable = False)
    
    def __init__(self, user_id, session_id, seat):
        self.user_id = user_id
        self.session_id = session_id
        self.reserve_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.get_ticket = False
        self.seat = seat
    
class food_record(db.Model):
    order_id = db.Column(db.Integer, primary_key = True)
    food_id = db.Column(db.Integer, primary_key = True)
    num = db.Column(db.Integer, unique = False, nullable = False)

    def __init__(self, order_id, food_id, num):
        self.order_id = order_id
        self.food_id = food_id
        self.num = num
        
class ticket_record(db.Model):
    order_id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.Integer, primary_key = True)
    num = db.Column(db.Integer, unique = False, nullable = False)
    
    def __init__(self, order_id, type, num):
        self.order_id = order_id
        self.type = type
        self.num = num
        
@app.route("/")
def home_page():
    connection = psycopg2.connect(database = "movie", user = "ming", password = "20020622", host = "localhost", port = "5432")
    cursor = connection.cursor()
    sql = '''SELECT * FROM CINEMA'''
    cursor.execute(sql)
    result = cursor.fetchall()
    
    return render_template("home.html", cinemas = result)

@app.route("/home")
def home():
    connection = psycopg2.connect(database = "movie", user = "ming", password = "20020622", host = "localhost", port = "5432")
    cursor = connection.cursor()
    sql = '''SELECT * FROM CINEMA'''
    cursor.execute(sql)
    result = cursor.fetchall()
    
    return render_template("home.html", cinemas = result)

@app.route("/author/<id>", methods=["GET", "POST"])
def author(id):
    connection = psycopg2.connect(database = "movie", user = "ming", password = "20020622", host = "localhost", port = "5432")
    cursor = connection.cursor()
    
    n_id = int(id)
    cursor.execute("SELECT * FROM cinema WHERE cinema.id='%s'", [n_id])
    result = cursor.fetchall()
    
    cursor.execute(f'''SELECT * FROM session WHERE cinema = {n_id}''')
    sessions = cursor.fetchall()
    
    movies = collections.defaultdict(lambda: collections.defaultdict(list))
    for session in sessions:
        cursor.execute(f'''SELECT name, theater_type from movie WHERE id = {session[1]}''')
        movies[session[4]][cursor.fetchall()[0]].append(session)
    
    return render_template("author.html", cinema = result, sessions = sessions, movies = movies)

@app.route("/explore", methods = ["GET", "POST"])
def explore():
    connection = psycopg2.connect(database = "movie", user = "ming", password = "20020622", host = "localhost", port = "5432")
    cursor = connection.cursor()
    sql = '''SELECT * FROM movie'''
    cursor.execute(sql)
    result = cursor.fetchall()
    return render_template("explore.html", length = len(result), movies = result)

@app.route("/movie_info/<name_ch>/<name_en>/<mv_on>/<director>/<actor>/<type>/<long>/<intro>/<image>", methods = ["GET", "POST"])
def movie_info(name_ch, name_en, mv_on, director, actor, type, long, intro, image):
    trailer = request.args.get("trailer")
    movie = [name_ch, name_en, mv_on, director, actor, type, int(long) // 60, int(long) % 60, intro, image, trailer]
    
    return render_template("movie_info.html", movie = movie)

@app.route("/details")
def details():
    if (login):
        global name, mail, phone, birth, points, level
        return render_template("details.html", name = name, mail = mail, phone = phone, birth = birth, points = points, level = level)
    else:
        return render_template("ask_login.html")

@app.route("/create")
def create():
    return render_template("create.html", message = False)

@app.route("/check_login", methods = ["POST"])
def check_login():
    mail_local = request.form.get("mail")
    password = request.form.get("password")
    
    connection = psycopg2.connect(database = 'movie', user = 'ming', password = '20020622', host = 'localhost', port = '5432')
    cursor = connection.cursor()
    
    sql = f'''SELECT password FROM users
            WHERE users.mail = '{mail_local}';'''
    
    cursor.execute(sql)
    result = cursor.fetchall()
    
    if (not result):
        return render_template("create.html", message = "The pair of mail and password does not exist.")
    elif (result[0][0] == password):
        global login,uid,  name, mail, phone, birth, points, level
        login = True
        sql = f'''SELECT uid, name, mail, phone, birth, points, level FROM users
                WHERE users.mail = '{mail_local}';'''
        cursor.execute(sql)
        result = cursor.fetchall()
        uid, name, mail, phone, birth, points, level = result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], result[0][5], result[0][6]
        return render_template("details.html", name = name, mail = mail, phone = phone, birth = birth, points = points, level = level)
    else:
        return render_template("create.html", message = "The password is incorrect.")

@app.route("/register")
def register():
    return render_template("register.html", message = False)

@app.route("/check_register", methods = ["GET", "POST"])
def check_register():
    id = request.form.get("id")
    name = request.form.get("name")
    birth = request.form.get("birth")
    phone = request.form.get("phone")
    mail = request.form.get("mail")
    password = request.form.get("password")
    
    if (len(id) != 10 or not id[0].isupper() or not id[1: ].isnumeric()):
        message = "The format of id card is incorrect."
    elif (len(name) > 20):
        message = "The length of name must smaller than 10."
    elif (len(birth) != 8 or not birth.isnumeric()):
        message = "The format of birth is incorrect."
    elif (len(phone) != 10 or not phone.isnumeric()):
        message = "The format of phone is incorrect."
    elif (len(password) > 10):
        message = "The length of password must smaller than 10."
    else:
        connection = psycopg2.connect(database = 'movie', user = 'ming', password = '20020622', host = 'localhost', port = '5432')
        cursor = connection.cursor()
        
        try:
            sql1 = f'''SELECT EXISTS(
                        SELECT 1 FROM users
                        WHERE idcard = '{id}');'''
            cursor.execute(sql1)
            result = cursor.fetchall()
            if (result[0][0]):
                message = "The idcard had registered."
                return render_template("register.html", message = message)
        except:
            pass
        try:
            sql2 = f'''SELECT EXISTS (
                        SELECT 1 FROM users
                        WHERE phone = '{phone}');'''
            cursor.execute(sql2)
            result = cursor.fetchall()
            if (result[0][0]):
                message = "The phone had registered."
                return render_template("register.html", message = message)
        except:
            pass
            
        try:
            sql3 = f'''SELECT uid EXISTS(
                        SELECT 1 FROM users
                        WHERE mail = '{mail}');'''
            cursor.execute(sql3)
            result = cursor.fetchall()
            if (result[0][0]):
                message = "The mail had registered."
                return render_template("register.html", message = message)
        except:
            pass
        
        p = users(idcard = id, name = name, birth = birth, phone = phone, mail = mail, password = password)
        db.session.add(p)
        db.session.commit()
        message = "Register success"
        
    return render_template("create.html", message = message)

@app.route("/forget_password")
def forget_password():
    return render_template("forget_password.html")

@app.route("/check_password", methods = ["GET", "POST"])
def check_password():
    mail = request.form.get("mail")
    id = request.form.get("id")
    
    connection = psycopg2.connect(database = "movie", user = "ming", password = "20020622", host = "localhost", port = "5432")
    cursor = connection.cursor()
    
    sql = f'''SELECT idcard, password FROM users
            WHERE mail = '{mail}';'''
    cursor.execute(sql)
    result = cursor.fetchall()
    
    if (not result):
        message = "The pair of idcard and the mail does not exist."
    elif (result[0][0] != id):
        message = "The idcard does not correspond to the mail."
    else:
        message = f"Your password is {result[0][1]}"
        
    return render_template("create.html", message = message)

@app.route("/info_revise", methods = ["GET", "POST"])
def info_revise():
    global name, mail, phone, birth, points, level
    return render_template("info_revise.html", message = False, name = name, mail = mail, phone = phone, birth = birth, points = points, level = level)

@app.route("/check_info_revise", methods = ["GET", "POST"])
def check_info_revise():
    global uid, name, mail, phone, birth, points, level
    phone_local = request.form.get("phone")
    birth_local = request.form.get("birth")
    password_local = request.form.get("password")
    mail_local = request.form.get("mail")
    
    if (phone_local or birth_local or password_local or mail_local):
        sql = '''UPDATE users SET '''
        if (phone_local):
            if (len(phone_local) != 10 or not phone_local.isnumeric()):
                return render_template("info_revise.html", message = "The format of phone is incorrect.", name = name, mail = mail, phone = phone, birth = birth, points = points)
            phone = phone_local
            sql += f'''phone = '{phone_local}', '''
        if (birth_local):
            if (len(birth_local) != 8 or not birth_local.isnumeric()):
                return render_template("info_revise.html", message = "The format of birth is incorrect.", name = name, mail = mail, phone = phone, birth = birth, points = points)
            birth = birth_local
            sql += f'''birth = '{birth_local}', '''
        if (password_local):
            if (len(password_local) > 10):
                return render_template("info_revise.html", message = "The length of password must smaller than 10.", name = name, mail = mail, phone = phone, birth = birth, points = points)
            password = password_local
            sql += f'''password = '{password_local}', '''
        if (mail_local):
            mail = mail_local
            sql += f'''mail = '{mail_local}', '''
        sql = sql[: -2]
        sql += f''' WHERE uid = {uid};'''
        
        connection = psycopg2.connect(database = "movie", user = "ming", password = "20020622", host = "localhost", port = "5432")
        cursor = connection.cursor()
        
        cursor.execute(sql)
        connection.commit()
        message = "The changes have completed."
    else:
        message = "Please key in some changes."
    return render_template("info_revise.html", message = message, name = name, mail = mail, phone = phone, birth = birth, points = points, level = level)

@app.route("/record")
def record():
    global uid
    connection = psycopg2.connect(database = "movie", user = "ming", password = "20020622", host = "localhost", port = "5432")
    cursor = connection.cursor()
    
    sql = f'''SELECT movie.name, session.room, session.period, cinema.name, orders.reserve_date, orders.get_ticket, orders.seat, orders.numbering FROM orders, cinema, session, movie
            WHERE {uid} = orders.user_id and orders.session_id = session.id and session.cinema = cinema.id and session.movie_id = movie.id'''
    cursor.execute(sql)
    result = cursor.fetchall()
    global record
    record = result
    
    return render_template("record.html", result = result, length = len(result))

@app.route("/record_revise/<movie>/<theater>/<period>/<cinema>/<seat>/<numbering>", methods = ["GET", "POST"])
def record_revise(movie, theater, period, cinema, seat, numbering):
    result = [movie, theater, period[: -3], cinema, seat, numbering]
    global order_numbering
    order_numbering = numbering
    
    return render_template("record_revise.html", result = result)

@app.route("/delete_order", methods = ["GET", "POST"])
def delete_order():
    global order_numbering
    connection = psycopg2.connect(database = "movie", user = "ming", password = "20020622", host = "localhost", port = "5432")
    cursor = connection.cursor()
    
    sql1 = f'''DELETE FROM food_record
            WHERE order_id = '{order_numbering}';'''
    cursor.execute(sql1)
            
    sql2 = f'''DELETE FROM ticket_record
            WHERE order_id = '{order_numbering}';'''
    cursor.execute(sql2)
        
    sql3 = f'''DELETE FROM orders 
            WHERE numbering = '{order_numbering}';'''
    cursor.execute(sql3)
    
    connection.commit()
    
    return redirect(url_for("record"))

@app.route("/check_record_revise", methods = ["GET", "POST"])
def check_record_revise():
    global order_numbering
    connection = psycopg2.connect(database = "movie", user = "ming", password = "20020622", host = "localhost", port = "5432")
    cursor = connection.cursor()
    type = request.form.get("radio")
    
    sql = f'''UPDATE ticket_record SET type = 1 WHERE order_id = '{order_numbering}';'''
    cursor.execute(sql)
    
    connection.commit()
    
    return render_template("home.html")
        


@app.route("/ticket")
def ticket():
    if (login):
        connection = psycopg2.connect(database = "movie", user = "ming", password = "20020622", host = "localhost", port = "5432")
        cursor = connection.cursor()
        
        sql1 = '''SELECT name from cinema'''
        cursor.execute(sql1)
        result1 = cursor.fetchall()
        
        sql2 = '''SELECT name from movie'''
        cursor.execute(sql2)
        result2 = cursor.fetchall()
        
        return render_template("ticket.html", cinemas = result1, length1 = len(result1), movies = result2, length2 = len(result2))
    else:
        return render_template("ask_login.html")

@app.route("/select_seat", methods = ["GET", "POST"])
def select_seat():
    if (login):
        cinema = request.form.get("cinema")
        movie = request.form.get("movie")
        date = request.form.get("date")
        people = int(request.form.get("people"))
        time = request.form.get("time")
        if (cinema == "0" or movie == "0" or  date == "0" or people == "0" or time == "0"):
            return redirect(url_for("ticket"))
        
        return render_template("select_seat.html", cinema = cinema, movie = movie, date = "2023-01-" + date, people = people, time = time)
    else:
        return render_template("ask_login.html")

@app.route("/ticket_detail/<movie>/<cinema>/<date>/<people>/<time>", methods = ["GET", "POST"])
def ticket_detail(movie, cinema, date, people, time):
    if (login):
        type = request.form.get("type")
        seats = []
        for i in range(int(people)):
            seat_row = request.form.get(f"select_row{i}")
            seat_num = request.form.get(f"select_num{i}")
            
            if (not seat_row or not seat_num):
                connection = psycopg2.connect(database = "movie", user = "ming", password = "20020622", host = "localhost", port = "5432")
                cursor = connection.cursor()
                
                sql1 = '''SELECT name from cinema'''
                cursor.execute(sql1)
                result1 = cursor.fetchall()
                
                sql2 = '''SELECT name from movie'''
                cursor.execute(sql2)
                result2 = cursor.fetchall()
                
                return render_template("select_seat.html", cinema = cinema, movie = movie, date = date, people = int(people), time = time)
            
            seat = seat_row + seat_num
            seats.append(seat)
        
        return render_template("ticket_detail.html", movie = movie, cinema = cinema, date = date, people = people, type = type, seats = seats, time = time)
    else:
        return render_template("ask_login.html")
        
@app.route("/ticket_food/<movie>/<cinema>/<date>/<people>/<time>/<type>/<seats>", methods = ["GET", "POST"])
def ticket_food(movie, cinema, date, people, time, type, seats):
    if (login):
        connection = psycopg2.connect(database = "movie", user = "ming", password = "20020622", host = "localhost", port = "5432")
        cursor = connection.cursor()
        
        sql = '''SELECT * from food order by id'''
        cursor.execute(sql)
        food = cursor.fetchall()
        
        return render_template("ticket_food.html", movie = movie, cinema = cinema, date = date, people = people, type = type, food = food, length = len(food), time = time, seats = seats)
    else:
        return render_template("ask_login.html")

@app.route("/ticket_total/<movie>/<cinema>/<date>/<people>/<type>/<time>/<seats>", methods = ["GET", "POST"])
def ticket_total(movie, cinema, date, people, type, time, seats):
    if (login):
        id = {}
        for i in range(1, 9):
            n = request.form.get(str(i))
            if (n != '0'):
                id[i] = int(n)
            
        connection = psycopg2.connect(database = "movie", user = "ming", password = "20020622", host = "localhost", port = "5432")
        cursor = connection.cursor()
        
        food = []
        for n in id:
            sql = f'''SELECT name, price from food
                    WHERE id = {int(n)};'''
            cursor.execute(sql)
            temp = []
            t = cursor.fetchall()
            temp.append(t[0][0])
            temp.append(t[0][1])
            temp.append(id[n])
            food.append(temp)
        
        temp = []
        t = ""
        print(seats)
        for s in seats:
            if (s == ","):
                temp.append(t)
                t = ""
                continue
            if (s not in ["[", "\'", "]", " "]):
                t += s
        temp.append(t)
        print(temp)
        
        return render_template("ticket_total.html", movie = movie, cinema = cinema, date = date, people = int(people), type = type, food = food, length = len(food), time = time, seats = temp)
    else:
        return render_template("ask_login.html")
        
@app.route("/ticket_confirm/<movie>/<cinema>/<date>/<people>/<type>/<food>/<time>/<seats>", methods = ["GET", "POST"])
def ticket_confirm(movie, cinema, date, people, type, food, time, seats):
    connection = psycopg2.connect(database = "movie", user = "ming", password = "20020622", host = "localhost", port = "5432")
    cursor = connection.cursor()
    
    sql1 = f'''SELECT id from movie where name = '{movie}';'''
    cursor.execute(sql1)
    movie_id = cursor.fetchall()[0][0]
    sql2 = f'''SELECT id from cinema where name = '{cinema}';'''
    cursor.execute(sql2)
    cinema_id = cursor.fetchall()[0][0]
    time = datetime.datetime.strptime(time, "%H:%M").time()

    sql3 = f'''SELECT id from session WHERE movie_id = {movie_id} and period = '{time}' and datetime = '{date}' and cinema = '{cinema_id}';'''
    cursor.execute(sql3)
    session_id = cursor.fetchall()[0][0]
    
    p1 = orders(uid, session_id, seats[2: 4])
    db.session.add(p1)
    db.session.commit()
    sql4 = f'''SELECT numbering from orders where user_id = {uid} and session_id = {session_id} and seat = '{seats[2: 4]}';'''
    cursor.execute(sql4)
    order_id = cursor.fetchall()[0][0]
    
    t = ""
    temp = []
    for f in food:
        if (f == ","):
            temp.append(t)
            t = ""
            continue
        if (f not in ["[", "]", " ", "\'"]):
            t += f
    temp.append(t)
    
    for i in range(len(temp) // 3):
        sql5 = f'''SELECT id from food where name = '{temp[i * 3]}';'''
        cursor.execute(sql5)
        food_id = cursor.fetchall()[0][0]
        p2 = food_record(order_id, food_id, temp[i * 3 + 2])
        db.session.add(p2)
        db.session.commit()
    
    p3 = ticket_record(order_id, 4, people)
    db.session.add(p3)
    db.session.commit()
    
    return redirect("/explore")

if (__name__ == "__main__"):
    app.run()