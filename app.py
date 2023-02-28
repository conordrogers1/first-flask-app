from flask import Flask, render_template, request, g
import sqlite3


app = Flask(__name__)

def connect_db():
    sql = sqlite3.connect('app.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite3'):
        g.sqlite_db.close()


@app.route('/', methods=['GET', 'POST'])
def home():
    db = get_db()
    cur = db.execute('select * from people;')
    results = cur.fetchall()
    
    return render_template('index.html', results=results)


@app.route('/process', methods=['GET', 'POST'])
def process():
    name = request.form['name'].title()
    age = request.form['age']
    location = request.form['location'].title()
    
    db = get_db()
    
    # insert into the database
    if name and age and location:
        db.execute('insert into people (name, age, location) values (?, ?, ?)', [name, age, location])
        db.commit()
    
    cur = db.execute('select * from people;')
    results = cur.fetchall()
    
    return render_template('process.html', name=name, age=age, location=location, results=results)
    
    
if __name__ == '__main__':
    app.run(debug=True)