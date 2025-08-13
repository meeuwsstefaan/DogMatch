# Python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# models.py
class Matches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    field1 = db.Column(db.String(100))  # Placeholder: Replace with actual fields
    field2 = db.Column(db.String(100))  # Placeholder: Replace with actual fields


class ConfirmedMatches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    field1 = db.Column(db.String(100))  # Same fields as Matches
    field2 = db.Column(db.String(100))  # Same fields as Matches


class DogOwner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(40))

    dogs = db.relationship("Dog", backref="owner", cascade="all, delete-orphan")


class Dog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    breed = db.Column(db.String(80))
    owner_id = db.Column(db.Integer, db.ForeignKey("dog_owner.id"), nullable=False)

    availabilities = db.relationship(
        "Availability", backref="dog", cascade="all, delete-orphan"
    )


class DogWalker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(40))

    availabilities = db.relationship(
        "Availability", backref="walker", cascade="all, delete-orphan"
    )


class Availability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weekday = db.Column(db.Integer, nullable=False)  # 0 = Mon … 6 = Sun
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    dog_id = db.Column(db.Integer, db.ForeignKey("dog.id"))
    walker_id = db.Column(db.Integer, db.ForeignKey("dog_walker.id"))
