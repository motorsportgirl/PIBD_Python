from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)


# CONEXIUNE
def get_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Mihaela-2004',  # SCHIMBĂ CU PAROLA TA
        database='vfinala'
    )

@app.route('/')
def index():
    return render_template('index.html')

# SECTIUNEA AUTORI

@app.route('/autori', methods=['GET', 'POST']) #tipuri de cereri acceptate de sursa (get, post)
def autori():
    db = get_db()
    cursor = db.cursor(dictionary=True)  #returneaza datele sub forma de dictionar

    if request.method == 'POST':
        selected_id = request.form.get('selected_id')
        action = request.form.get('action')

        if not selected_id:
            return redirect(url_for('autori'))

        if action == 'sterge':
            cursor.execute("DELETE FROM autori WHERE IdAutor = %s", (selected_id,))
            db.commit()
            return redirect(url_for('autori'))

        elif action == 'modifica':
            return redirect(url_for('pagina_modifica_autor', id_autor=selected_id))

    cursor.execute("SELECT * FROM autori")
    date = cursor.fetchall()
    db.close()
    return render_template('autori/autori.html', date=date)


@app.route('/autori/adaugare')
def pagina_adauga_autor():
    return render_template('autori/adaugare.html')


@app.route('/autori/salveaza', methods=['POST'])
def salveaza_autor():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO autori (Nume, Data_nastere, Nationalitate) VALUES (%s, %s, %s)",
                   (request.form['nume'], request.form['data'], request.form['nat']))
    db.commit()
    db.close()
    return redirect(url_for('autori'))


@app.route('/autori/modificare/<int:id_autor>')
def pagina_modifica_autor(id_autor):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM autori WHERE IdAutor = %s", (id_autor,))
    autor = cursor.fetchone()
    db.close()
    return render_template('autori/modificare_a.html', autor=autor)


@app.route('/autori/update', methods=['POST'])
def update_autor():
    db = get_db()
    cursor = db.cursor()
    sql = "UPDATE autori SET Nume=%s, Data_nastere=%s, Nationalitate=%s WHERE IdAutor=%s"
    valori = (request.form['nume'], request.form['data'], request.form['nat'], request.form['id'])

    cursor.execute(sql, valori)
    db.commit()
    db.close()
    return redirect(url_for('autori'))


# SECTIUNEA CARTI

@app.route('/carti', methods=['GET', 'POST'])
def carti():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        selected_id = request.form.get('selected_id')
        action = request.form.get('action')
        if selected_id:
            if action == 'sterge':
                cursor.execute("DELETE FROM carti WHERE IdCarte = %s", (selected_id,))
                db.commit()
            elif action == 'modifica':
                return redirect(url_for('pagina_modifica_carte', id_carte=selected_id))
        return redirect(url_for('carti'))

    cursor.execute("SELECT * FROM carti")
    date = cursor.fetchall()
    db.close()
    return render_template('carti/carti.html', date=date)


@app.route('/carti/adaugare')
def pagina_adauga_carte():
    return render_template('carti/adaugare.html')


@app.route('/carti/salveaza', methods=['POST'])
def salveaza_carte():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO carti (Titlu, Editura, An_publicare, Categorie) VALUES (%s, %s, %s, %s)",
                   (request.form['titlu'], request.form['editura'], request.form['an'], request.form['cat']))
    db.commit()
    db.close()
    return redirect(url_for('carti'))


@app.route('/carti/modificare/<int:id_carte>')
def pagina_modifica_carte(id_carte):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM carti WHERE IdCarte = %s", (id_carte,))
    carte = cursor.fetchone()
    db.close()
    return render_template('carti/modificare.html', carte=carte)


@app.route('/carti/update', methods=['POST'])
def update_carte():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE carti SET Titlu=%s, Editura=%s, An_publicare=%s, Categorie=%s WHERE IdCarte=%s",
                   (request.form['titlu'], request.form['editura'], request.form['an'], request.form['cat'],
                    request.form['id']))
    db.commit()
    db.close()
    return redirect(url_for('carti'))



# SECTIUNEA BIBLIOTECI

@app.route('/biblioteci', methods=['GET', 'POST'])
def biblioteci():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        selected_id = request.form.get('selected_id')
        action = request.form.get('action')
        if not selected_id:
            return redirect(url_for('biblioteci'))
        if action == 'sterge':
            cursor.execute("DELETE FROM biblioteci WHERE IdBiblioteca = %s", (selected_id,))
            db.commit()
            return redirect(url_for('biblioteci'))
        elif action == 'modifica':
            return redirect(url_for('pagina_modifica_biblioteca', id_bib=selected_id))

    # JOIN pentru a face legatura intre tabele
    cursor.execute("""
        SELECT b.*, a.Nume as NumeAutor, c.Titlu as TitluCarte, 
               c.Editura, c.An_publicare 
        FROM biblioteci b 
        JOIN autori a USING(IdAutor) 
        JOIN carti c USING(IdCarte)
    """)
    date = cursor.fetchall()
    db.close()
    return render_template('biblioteci/biblioteci.html', date=date)


@app.route('/biblioteci/modificare/<int:id_bib>')
def pagina_modifica_biblioteca(id_bib):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    # JOIN pentru a vedea detaliile complete în pagina de editare
    cursor.execute("""
        SELECT b.*, a.Nume as NumeAutor, c.Titlu as TitluCarte, 
               c.Editura, c.An_publicare
        FROM biblioteci b 
        JOIN autori a USING(IdAutor)
        JOIN carti c USING(IdCarte)
        WHERE IdBiblioteca = %s
    """, (id_bib,))
    bib = cursor.fetchone()
    db.close()
    return render_template('biblioteci/modificare.html', bib=bib)

@app.route('/biblioteci/adaugare')
def pagina_adauga_biblioteca():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Luăm toți autorii pentru listă
    cursor.execute("SELECT IdAutor, Nume FROM autori ORDER BY Nume")
    autori = cursor.fetchall()

    # Luăm toate cărțile pentru listă
    cursor.execute("SELECT IdCarte, Titlu FROM carti ORDER BY Titlu")
    carti = cursor.fetchall()

    db.close()
    return render_template('biblioteci/adaugare.html', autori=autori, carti=carti)


@app.route('/biblioteci/salveaza', methods=['POST'])
def salveaza_biblioteca():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO biblioteci (IdAutor, IdCarte, Nume, Adresa, Nr_angajati) VALUES (%s, %s, %s, %s, %s)",
                   (request.form['id_a'], request.form['id_c'], request.form['nume'], request.form['adresa'],
                    request.form['nr']))
    db.commit()
    db.close()
    return redirect(url_for('biblioteci'))

@app.route('/biblioteci/update', methods=['POST'])
def update_biblioteca():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE biblioteci SET Nume=%s, Adresa=%s, Nr_angajati=%s WHERE IdBiblioteca=%s",
                   (request.form['nume'], request.form['adresa'], request.form['nr'], request.form['id']))
    db.commit()
    db.close()
    return redirect(url_for('biblioteci'))


if __name__ == '__main__':
    app.run(debug=True)