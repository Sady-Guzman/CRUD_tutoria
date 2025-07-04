from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Ruta para mostrar todos los autos
@app.route('/')
def index():
    conn = sqlite3.connect('autos.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM autos")
    autos = cursor.fetchall()
    conn.close()
    return render_template('index.html', autos=autos)

# Ruta para agregar un nuevo auto
@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        anio = request.form['anio']
        precio = request.form['precio']
        color = request.form['color']
        disponible = request.form['disponible']

        conn = sqlite3.connect('autos.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO autos (marca, modelo, anio, precio, color, disponible)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (marca, modelo, anio, precio, color, disponible)
        )
        conn.commit()
        conn.close()
        return redirect('/')

# Ruta para borrar un auto
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('autos.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM autos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# Ruta para actualizar un auto
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('autos.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        anio = request.form['anio']
        precio = request.form['precio']
        color = request.form['color']
        disponible = request.form['disponible']
        cursor.execute("""
            UPDATE autos SET marca=?, modelo=?, anio=?, precio=?, color=?, disponible=?
            WHERE id=?
        """, (marca, modelo, anio, precio, color, disponible, id))
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        cursor.execute("SELECT * FROM autos WHERE id = ?", (id,))
        auto = cursor.fetchone()
        conn.close()
        return render_template('edit.html', auto=auto)

if __name__ == '__main__':
    app.run(debug=True)
