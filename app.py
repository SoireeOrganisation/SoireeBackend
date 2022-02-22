from flask import Flask, request, jsonify, make_response

from db import db, Review, Category, User, Role, Company, Bonus, update_session
from config import Config

from apiflask import APIFlask

app = APIFlask(__name__, spec_path='/spec')
app.config['SPEC_FORMAT'] = 'yaml'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soiree.db'
app.config.from_object(Config())
db.app = app
db.init_app(app)
try:
    db.create_all()
    r = Role(name='Тест')
    c = Company(name='Рога и копыта')
    cat = Category(name='Доброжелательность')
    u1 = User(name='A', surname='A1', login='aa')
    u1.set_password("123")
    u2 = User(name='B', surname='B1', login='bb')
    u2.set_password("123")
    u1.company = c
    u2.company = c
    bonus = Bonus(name='Электрокочерга')
    u2.bonuses.append(bonus)
    u1.bonuses.append(bonus)
    rev = Review(note='123', score=10)
    rev.reviewer = u1
    rev.subject = u2
    rev.company = c
    rev.category = cat
    update_session(r, c, cat, u1, u2, rev, bonus)
except Exception as e:
    print(e)
    print("error was occurred")


def is_valid_key(key):
    return User.query.filter_by(key=key).first() is not None


@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.json
    if data.get("key") is None:
        return make_response(jsonify('"key" field missing'), 400)
    return jsonify({"status": "ok" if is_valid_key(data.get("key")) else "bad"})


@app.route("/api/staff", methods=["GET"])
def api_staff():
    key = request.args.get("key")
    if key is None:
        return make_response(jsonify('"key" field missing'), 400)
    print(key)
    if not is_valid_key(key):
        return make_response(jsonify('Bad key'), 403)

    user = User.query.filter_by(key=key).first()
    company_id = user.company_id
    staff = User.query.filter_by(company_id=company_id).all()
    staff = [employee.to_public_dict() for employee in staff]
    return make_response(jsonify(staff), 200)


@app.route("/api/reviews", methods=["GET", "POST"])
def api_reviews():
    if request.method == "GET":
        key = request.args.get("key")
        if key is None:
            raise NotImplementedError()
        if not is_valid_key(key):
            raise NotImplementedError()
        return jsonify([review.to_public_dict() for review in Review.query.filter_by(subject_id=User.query.filter_by(key=key).first().id).all()], 200)
    elif request.method == "POST":
        data = request.json
        key = data.get("key")
        subject_id = data.get("subject_id")
        reviews = data.get("reviews")
        if not all([o is not None for o in [key, subject_id, reviews]]):
            raise NotImplementedError()
        if not is_valid_key(key):
            raise NotImplementedError()
        db_reviews = []
        for item in reviews:
            category_id = item.get("category_id")
            note = item.get("note")
            score = item.get("score")
            if not all([o is not None for o in [category_id, note, score]]):
                raise NotImplementedError()
            reviewer = User.query.filter_by(key=key).first()
            subject = User.query.filter_by(id=subject_id).first()
            category = Category.query.filter_by(id=category_id).first()
            company = Company.query.filter_by(id=reviewer.company_id).first()
            review = Review(note=note, score=score)
            review.reviewer = reviewer
            review.subject = subject
            review.category = category
            review.company = company

            db_reviews.append(review)
        update_session(*db_reviews)
        return make_response(jsonify("ok"), 200)


@app.route("/api/reviews/categories", methods=["GET"])
def api_categories():
    return make_response(jsonify([category.to_public_dict() for category in Category.query.all()]), 200)


@app.route("/api/bonuses", methods=["GET", "POST"])
def api_bonuses():
    if request.method == "GET":
        user_key = request.args.get("key")
    else:
        data = request.json
        user_key = data.get("key")
    if user_key is None:
        message = jsonify(message='key missing')
        return make_response(message, 400)
    user_bonuses = User.query.filter_by(key=user_key).first()
    if user_bonuses is None:
        message = jsonify(message='key missing')
        return make_response(message, 400)  # TODO: поменять код ошибки

    user_bonuses = [bonus.to_public_dict() for bonus in user_bonuses.bonuses]

    return make_response(jsonify(user_bonuses), 200)