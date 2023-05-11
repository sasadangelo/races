from . import db
from datetime import datetime

# Creating model table for our CRUD database
class Race(db.Model):
   __tablename__ = "race"
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   name = db.Column(db.String(50))
   time = db.Column(db.DateTime, default=datetime.utcnow)
   city = db.Column(db.String(20))
   distance = db.Column(db.Integer)
   website = db.Column(db.String(20))

   def to_json(self):
      return {
         'id': self.id,
         'name': self.name,
         'time': self.time,
         'city': self.city,
         'distance': self.distance,
         'website': self.website
      }

   def __init__(self, name, time, city,
                      distance, website):
       self.name = name
       self.time = time
       self.city = city
       self.distance = distance
       self.website = website
