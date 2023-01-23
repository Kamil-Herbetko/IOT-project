from datetime import datetime
from website import db
from enum import Enum, unique


class Status(Enum):
    dostarczona = "Dostarczona"
    nadana = "Nadana"


class Kurier(db.Model):
    __tablename__ = "Kurier"

    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(30), unique=True, nullable=False)


    def __repr__(self):
        return f"Kurier {self.id}, {self.nazwa}"


class Paczka(db.Model):
    __tablename__ = "Paczka"

    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(30), unique=True, nullable=False, default=None)

    def __repr__(self):
        return f"Paczka {self.id}, {self.nazwa}"


class Dostarczenia(db.Model):
    __tablename__ = "Dostarczenia"
    kurier_id = db.Column(
        db.Integer, db.ForeignKey("Kurier.id"), primary_key=True, nullable=False
    )
    paczka_id = db.Column(
        db.Integer, db.ForeignKey("Paczka.id"), primary_key=True, nullable=False
    )
    dataUtworzenia = db.Column(db.DateTime, nullable=False, default=datetime.now())
    status = db.Column(db.Enum(Status), nullable=False)

    def __repr__(self):
        return f"Dostarczenie: {self.status}, {self.dataUtworzenia}"
