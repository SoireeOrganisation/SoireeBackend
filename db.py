import hashlib

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


user_bonus = db.Table('bonuses',
    db.Column('bonus_id', db.Integer, db.ForeignKey('bonus.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=False)
    surname = db.Column(db.String(128), nullable=False, unique=False)
    patronymic = db.Column(db.String(128), unique=False, default="")
    login = db.Column(db.String(50), index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    key = db.Column(db.String(256), index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    reviewed = db.relationship('Review', backref=db.backref('reviewer', lazy=True), foreign_keys='Review.reviewer_id')
    subjected = db.relationship('Review', backref=db.backref('subject', lazy=True), foreign_keys='Review.subject_id')
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    bonuses = db.relationship('Bonus', secondary=user_bonus, lazy='subquery', backref=db.backref('users', lazy=True))

    @hybrid_property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, new_password):
        if new_password:
            self.set_password(new_password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        self.key = hashlib.md5((password + self.login).encode("utf-8")).hexdigest()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_public_dict(self):
        return {"id": self.id, "name": self.name, "surname": self.surname,
                "patronymic": self.patronymic, "company": self.company.to_public_dict()}

    def __repr__(self):
        return "{} | {} {} {}".format(self.login,
                                      self.name,
                                      self.surname,
                                      self.patronymic)


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)
    staff = db.relationship('User', backref='company', lazy=True)
    reviews = db.relationship('Review', backref='company', lazy=True)

    def to_public_dict(self):
        return {'id': self.id, 'name': self.name}

    def __repr__(self):
        return "{}".format(self.name)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)
    users = db.relationship('User', backref='role', lazy=True)

    def __repr__(self):
        return "{}".format(self.name)


class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    note = db.Column(db.Text)
    score = db.Column(db.Integer, nullable=False)

    def to_public_dict(self):
        return {"id": self.id, "category": self.category.to_public_dict(),
                "company": self.company.to_public_dict(),
                "reviewer": self.reviewer.to_public_dict(),
                "subject": self.subject.to_public_dict(),
                "note": self.note,
                "score": self.score}


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)
    reviews = db.relationship('Review', backref='category', lazy=True)

    def to_public_dict(self):
        return {"id": self.id, "name": self.name}

    def __repr__(self):
        return "{}".format(self.name)


class Bonus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)

    def to_public_dict(self):
        return {"id": self.id, "name": self.name}

    def __repr__(self):
        return "{}".format(self.name)


def update_session(*args):
    for el in args:
        db.session.add(el)
    db.session.commit()
