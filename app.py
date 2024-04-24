from flask import Flask, request, render_template, redirect, url_for
import sqlite3 

app = Flask(__name__)



import sqlite3

def get_db_connection():
    connection = sqlite3.connect('blog.db')
    connection.row_factory = sqlite3.Row
    connection.execute("""
        CREATE TABLE IF NOT EXISTS blogs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        title TEXT NOT NULL,
        content TEXT NOT NULL)""")
    return connection


@app.route('/')
def index():
    conn = get_db_connection()
    blogs = conn.execute('SELECT * FROM blogs').fetchall()
    conn.close()
    return render_template('index.html', blogs=blogs)



@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        conn = get_db_connection()
        conn.execute('INSERT INTO blogs (title, content) VALUES (?, ?)',
                         (title, content))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('create.html')

@app.route('/edit/<int:id>') 
def edit(id):
    conn = get_db_connection()
    blog = conn.execute('SELECT * FROM blogs WHERE id = ?', (id,)).fetchone()
    return render_template('edit.html', blog=blog)


@app.route('/update/<id>', methods=['POST', 'GET'])
def update(id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = get_db_connection()
        conn.execute('UPDATE blogs SET title = ?, content = ? WHERE id = ?',
                         (title, content, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return redirect(url_for('index'))


@app.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM blogs WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
