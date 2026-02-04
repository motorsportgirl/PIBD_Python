Gestiune Bibliotecă - Proiect PIBD (Python & Flask)
Acest proiect reprezintă o aplicație web funcțională destinată gestionării unei baze de date relaționale pentru o bibliotecă, dezvoltată ca parte a cursului de Programarea Interfețelor pentru Baze de Date.

🚀 Tehnologii Utilizate

Limbaj: Python.
Framework Web: Flask (utilizând motorul de template-uri Jinja2 și Werkzeug).
Bază de Date: MySQL (SGBD relațional).
Interfață (Frontend): Pico.css (pentru un design modern, minimalist și responsive).

📊 Modelul Bazei de Date
Aplicația gestionează o relație de tip M:N (Mulți-la-Mulți) între două entități principale, implementată printr-o tabelă de legătură:
Autori: IdAutor, Nume, Data_nastere, Nationalitate.
Cărți: IdCarte, Titlu, Editura, An_publicare, Categorie.
Biblioteci (Tabela de legătură): Gestionează asocierile dintre autori și cărți, incluzând detalii suplimentare precum numele bibliotecii, adresa și numărul de angajați.

🛠️ Funcționalități (CRUD)
Aplicația oferă o interfață completă pentru operațiunile esențiale asupra datelor:
Vizualizare (Read): Afișarea datelor sub formă de tabel, utilizând interogări de tip JOIN pentru a prezenta informații corelate (ex: numele autorului în dreptul cărții).
Adăugare (Create): Formulare cu dropdown-uri populate dinamic din baza de date pentru selectarea autorilor și a cărților.
Modificare (Update): Editarea înregistrărilor existente prin formulare pre-completate.
Ștergere (Delete): Eliminarea înregistrărilor, cu gestionarea integrității datelor (ștergerea în cascadă a referințelor din tabela de legătură).

📂 Structura Proiectului
Proiectul urmează o arhitectură apropiată de modelul MVC (Model-View-Controller):
app.py: Controller-ul principal care gestionează rutele, serverul web și logica de acces la date.
templates/: Conține vizualizările (View) structurate pe subfoldere (autori, biblioteci, carti).
static/: Fișiere de stil și resurse grafice.
.venv/: Mediul virtual Python (trebuie ignorat la commit).