from ext import db, app, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.ForeignKey("product_category.id"))
    name = db.Column(db.String)
    price = db.Column(db.Float)
    img = db.Column(db.String)


class ProductCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)

    def __init__(self, username, password, role="user"):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role

    def check_password_hash(self, password):
        return check_password_hash(self.password, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        category1 = ProductCategory(name="Phone")
        category2 = ProductCategory(name="Laptop")
        category3 = ProductCategory(name="SmartWatch")
        category4 = ProductCategory(name="tablet")
        category5 = ProductCategory(name="Monitor")

        db.session.add_all([category1, category2, category3, category4, category5])
        db.session.commit()

        new_user = User(username="Giorgi", password="adminpassword123", role="admin")
        db.session.add(new_user)

        db.session.commit()
