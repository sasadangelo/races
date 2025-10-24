# Races – Running Event Management in the Province of Rome

**Races** is a web application written in **Python** using **Flask** and **SQLite**, designed to manage running events in the province of Rome.
The app allows users to easily add, browse, and manage running events through a simple web interface.

---

## Technologies Used

[Flask](https://flask.palletsprojects.com/)
 – Python micro web framework

[SQLite](https://www.sqlite.org/)
 – lightweight relational database

[Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
 – ORM integration with SQLAlchemy

---

## Installation

Clone the repository and move into the project directory:

```bash
git clone https://github.com/sasadangelo/races.git
cd races
```


Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install the dependencies:

```bash
pip3 install -r requirements.txt
```

## Running the Application

Start the application using the run.sh script:

```bash
./run.sh
```

The script runs Flask in development mode.
By default, the app will be available at:

```
http://127.0.0.1:5000
```

## Live Demo

You can try the live demo of the web application at
👉 [sasadangelo.pythonAnywhere.com](https://sasadangelo.pythonanywhere.com)
