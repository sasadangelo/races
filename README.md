# Races – Gestione corse podistiche nella provincia di Roma

**Races** è una web application scritta in **Python** con **Flask** e **SQLite** che permette di gestire le corse podistiche della provincia di Roma.
L’app è pensata per inserire, consultare e amministrare eventi di corsa in modo semplice, tramite interfaccia web.

---

## Tecnologie utilizzate
- [Flask](https://flask.palletsprojects.com/) – micro web framework in Python
- [SQLite](https://www.sqlite.org/) – database relazionale leggero
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) – integrazione ORM con SQLAlchemy

---

## Installazione

Clona il repository e spostati nella cartella del progetto:

```bash
git clone https://github.com/sasadangelo/races.git
cd races
```

Crea e attiva un virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Installa le dipendenze:

```bash
pip3 install -r requirements.txt
```

## Esecuzione

Avvia l’applicazione tramite lo script run.sh:

```bash
./run.sh
```


Lo script esegue Flask in modalità sviluppo.
Per default, l’app sarà disponibile su:

```
http://127.0.0.1:5000
```

## Demo Live

Puoi provare la demo live della web application su [sasadangelo.pythonAnywhere.com](https://sasadangelo.pythonanywhere.com)