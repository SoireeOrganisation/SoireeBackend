import os

from flask import request, jsonify, make_response, flash, \
    render_template, redirect, url_for
from flask_login import LoginManager, login_user, \
    current_user, logout_user, login_required
from flask_admin import Admin
from sqlalchemy.sql.functions import func
from apiflask import APIFlask

from .models import db, Review, Category, User, Company, Bonus,\
    update_session, init_db
from .config import Config
from .login_form import LoginForm
from .admin_links import LoginMenuLink, LogoutMenuLink
from .admin_view_models import ReviewModelView, UserModelView,\
    CompanyModelView, CategoryModelView
from .mail_helpers import mail

app = APIFlask(__name__, spec_path='/spec')
app.config['SPEC_FORMAT'] = 'yaml'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///soiree.db")
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'implicit_returning': False}
app.config.from_object(Config())
db.app = app
db.init_app(app)
mail.app = app
mail.init_app(app)

try:
    init_db()
except Exception as e:
    print(e.__traceback__)
    print("error was occurred")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

admin = Admin(app)
admin.add_view(UserModelView(User, db.session))
admin.add_view(CompanyModelView(Company, db.session))
admin.add_view(CategoryModelView(Category, db.session))
admin.add_view(ReviewModelView(Review, db.session))
admin.add_link(LogoutMenuLink(name='Logout', category='', url="/logout"))
admin.add_link(LoginMenuLink(name='Login', category='', url="/login"))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        route = '/admin' if current_user.role_id == 1 else '/index'
        response = make_response(redirect(route))
        response.set_cookie("key", current_user.key)
        return response
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.username.data).first()
        if user is None:
            flash('User not found', category='danger')
            return redirect(url_for('login'))
        elif user.check_password(form.password.data) is False:
            flash('Invalid Username or password', category='danger')
            return redirect(url_for('login'))
        else:
            login_user(user)
            flash('Logged in successfully', category='success')
            route = '/admin' if user.role_id == 1 else '/index'
            response = make_response(redirect(route))
            response.set_cookie("key", user.key)
            return response
    for errors in form.errors.values():
        for error in errors:
            flash(error, category='danger')
    return render_template('login.html', form=form, title='Authorization')


def is_valid_key(key):
    return User.query.filter_by(key=key).first() is not None


@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.json
    if data.get("key") is None:
        return make_response(jsonify('"key" field missing'), 400)
    return jsonify(
        {"status": "ok" if is_valid_key(data.get("key")) else "bad"})


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
    staff = User.query.filter((User.company_id == company_id)
                              & (User.id != user.id)
                              & (User.role_id == 3)).all()
    staff = [employee.to_public_dict() for employee in staff]
    return make_response(jsonify(staff), 200)


@app.route("/forbidden")
def forbidden():
    return render_template("forbidden.html")


@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
@app.route("/dashboard", methods=["GET"])
def index():
    if not current_user.is_authenticated:
        return redirect('login')
    if current_user.role_id != 2:
        return redirect("/forbidden")
    total_reviews_count = db.session.query(
        func.count(Review.id).label('number')).filter(
        (Review.company_id == current_user.company_id)).first().number

    positive_reviews_count = db.session.query(
        func.count(Review.id).label('number')).filter(
        (Review.company_id == current_user.company_id) & (
                    Review.score > 5)).first().number

    negative_reviews_count = total_reviews_count - positive_reviews_count

    mean_reviews_count = db.session.query(
        func.avg(Review.score).label('average')).filter_by(
        company_id=current_user.company_id).first().average
    mean_reviews_count = round(mean_reviews_count, 2) \
        if mean_reviews_count is not None else 0

    staff = User.query.filter((User.role_id == 3)).all()

    return render_template("chief_dashboard.html",
                           company=current_user.company,
                           totalReviewsValue=total_reviews_count,
                           positiveReviewsValue=positive_reviews_count,
                           negativeReviewsValue=negative_reviews_count,
                           meanReviewsValue=mean_reviews_count,
                           percentage=int((mean_reviews_count / 10) * 100),
                           staff=staff)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/api/reviews", methods=["GET", "POST"])
def api_reviews():
    if request.method == "GET":
        key = request.args.get("key")
        if key is None:
            return make_response(jsonify('"key" field missing'), 400)
        if not is_valid_key(key):
            return make_response(jsonify('"key" is not valid'), 400)
        user = User.query.filter_by(key=key).first()
        if user.role_id != 3:
            query = Review.query.filter_by(company_id=user.company_id)
            page_size = request.args.get("pageSize")
            page = request.args.get("page")
            print(page_size, page)
            if page_size:
                query = query.limit(int(page_size))
            if page and page_size:
                query = query.offset((int(page) - 1) * int(page_size))
            return make_response(jsonify([review.to_public_dict() for review in
                                          query.all()]), 200)

        return make_response(jsonify([review.to_public_dict() for review in
                                      Review.query.filter_by(
                                          subject_id=User.query.filter_by(
                                              key=key).first().id).all()]),
                             200)
    elif request.method == "POST":
        data = request.json
        key = data.get("key")
        subject_id = data.get("subject_id")
        reviews = data.get("reviews")
        if not all([o is not None for o in [key, subject_id, reviews]]):
            return make_response(jsonify('There is empty fields'), 400)
        if not is_valid_key(key):
            return make_response(jsonify('"key" is not valid'), 400)
        db_reviews = []
        for item in reviews:
            category_id = item.get("category_id")
            note = item.get("note")
            score = item.get("score")
            if not all([o is not None for o in [category_id, note, score]]):
                return make_response(jsonify('There is empty fields'), 400)
            reviewer = User.query.filter_by(key=key).first()
            subject = User.query.filter_by(id=subject_id).first()
            if reviewer.id == subject.id:
                return make_response(
                    jsonify('reviewer and subject'
                            ' should not be the same person'),
                    400)
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
    return make_response(jsonify(
        [category.to_public_dict() for category in Category.query.all()]), 200)


@app.route("/api/bonuses", methods=["GET", "POST"])
def api_bonuses():
    if request.method == "GET":
        user_key = request.args.get("key")
    else:
        data = request.json
        user_key = data.get("key")
        if not is_valid_key(user_key):
            message = jsonify(message='invalid key')
            return make_response(message, 400)
        name = data.get("name")
        user_id = int(data.get("userId", "0"))
        if any(not x for x in [name, user_id]):
            message = jsonify(message='invalid data')
            return make_response(message, 400)
        new_bonus = Bonus(name=name)
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            message = jsonify(message='invalid userId')
            return make_response(message, 400)
        user.bonuses.append(new_bonus)
        update_session(user, new_bonus)
    if user_key is None:
        message = jsonify(message='key missing')
        return make_response(message, 400)
    user_bonuses = User.query.filter_by(key=user_key).first()
    if user_bonuses is None:
        message = jsonify(message='key missing')
        return make_response(message, 400)

    user_bonuses = [bonus.to_public_dict() for bonus in user_bonuses.bonuses]

    return make_response(jsonify(user_bonuses), 200)
