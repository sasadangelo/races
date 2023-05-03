from app import db
from app.races_api import app
from app.races import Race 

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Race=Race)
