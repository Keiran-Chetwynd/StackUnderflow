from flask import Flask, render_template, request, redirect, url_for
import sqlite3



app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
def create_database():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS your_table (
                id INTEGER PRIMARY KEY,
                name TEXT,
                info TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''')
    conn.commit()
    conn.close()

# Run this once to update your database
create_database()
@app.route('/')
def index():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM your_table').fetchall()
    conn.close()
    return render_template('index.html', rows=rows)

@app.route('/add', methods=['POST'])
def add_item():
    name = request.form['name']
    info = request.form['info']
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO your_table (name, info) 
        VALUES (?, ?)
    ''', (name, info))
    conn.commit()
    conn.close()
    return redirect(url_for('show_data'))

@app.route('/enter-data')
def data_enter():
    return render_template('data_enter.html')

@app.route('/show-data')
def show_data():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM your_table').fetchall()
    conn.close()
    return render_template('data_show.html', rows=rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)