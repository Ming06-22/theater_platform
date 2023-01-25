import psycopg2

tables = [
''' 
CREATE TABLE IF NOT EXISTS users(
    uid serial primary key,
    idcard varchar(10) not null,
    name varchar(20) not null,
    birth varchar(8) not null,
    phone varchar(10) not null,
    mail varchar(30) not null,
    password varchar(10) not null,
    points integer not null,
    level varchar(10) not null
)
''',
'''
CREATE TABLE IF NOT EXISTS movie(
    id serial primary key,
    name varchar(50) not null,
    name_english varchar(100) not null,
    length integer not null,
    mv_on varchar(10) not null,
    level varchar(5) not null,
    theater_type varchar(50) not null,
    director varchar(20),
    actor varchar(100),
    type varchar(20),
    intro varchar(5000),
    image varchar(100),
    trailer varchar(100)
)
''',
'''
CREATE TABLE IF NOT EXISTS cinema(
    id serial primary key,
    name varchar(25) not null,
    intro varchar(500),
    image varchar(100),
    name_en varchar(100),
    address varchar(100),
    phone varchar(20)
)
''',
'''
CREATE TABLE IF NOT EXISTS session(
    id serial primary key,
    movie_id integer REFERENCES movie(id),
    room varchar(1) not null,
    period time not null, 
    datetime date not null,
    cinema integer REFERENCES cinema(id)  
)
''',
'''
CREATE TABLE IF NOT EXISTS orders(
    numbering serial primary key,
    user_id integer REFERENCES users(uid),
    session_id integer REFERENCES session(id),
    reserve_date date,
    get_ticket bool,
    seat char(3)
)
''',
'''
CREATE TABLE IF NOT EXISTS food(
    id serial primary key,
    category varchar(5) not null,
    name varchar(20) not null,
    price integer not null,
    image varchar(100)
)
''',
'''
CREATE TABLE IF NOT EXISTS food_record(
    order_id int REFERENCES orders(numbering),
    food_id integer REFERENCES food(id),
    num integer not null,
    PRIMARY KEY(order_id, food_id)
)
''',
'''
CREATE TABLE IF NOT EXISTS ticket_type(
    id serial primary key,
    name varchar(20) not null,
    price integer not null,
    category varchar(6) not null,
    intro varchar(100)
)
''',
'''
CREATE TABLE IF NOT EXISTS ticket_record(
    order_id int REFERENCES orders(numbering),
    type integer REFERENCES ticket_type(id),
    num integer not null,
    PRIMARY KEY(order_id, type)
)
''',
'''
CREATE TABLE IF NOT EXISTS voucher(
    id serial primary key,
    points integer not null,
    stock integer not null,
    cinema integer REFERENCES cinema(id)
)
''',
'''
CREATE TABLE IF NOT EXISTS exchange_record(
    uid integer REFERENCES users(uid),
    vid integer REFERENCES voucher(id),
    status bool not null,
    exchange_date date not null,
    PRIMARY KEY(uid, vid)
)
'''
]

connection = psycopg2.connect(database = 'movie', user = 'ming', password = '20020622', host = 'localhost', port = '5432')
print("open success")

cursor = connection.cursor()
for table in tables:
    cursor.execute(table)

print("table create successfully")

connection.commit()
connection.close()