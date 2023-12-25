from os import path
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user

from forms import AddProductForm, RegisterForm, EditProductForm, LoginForm
from ext import app, db
from models import Product, ProductCategory, User

role = "mod"


@app.route("/")
def index():
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)

    if min_price is not None and max_price is not None:
        filtered_products = Product.query.filter(Product.price.between(min_price, max_price)).all()
    else:
        filtered_products = Product.query.all()

    return render_template('index.html', products=filtered_products, min_price=min_price, max_price=max_price)


@app.route("/product/<int:product_id>")
def view_product(product_id):
    chosen_product = Product.query.get(product_id)
    if chosen_product is None:
        return render_template("404.html")
    return render_template("product.html", product=chosen_product, role=role)


@app.route("/search/<string:name>")
def search(name):
    products = Product.query.filter(Product.name.ilike(f"%{name}%")).all()
    return render_template("search.html", products=products)


@app.route("/category/<int:category_id>")
def category(category_id):
    products = Product.query.filter(Product.category_id == category_id).all()
    return render_template("index.html", products=products)


@app.route("/add_product", methods=["POST", "GET"])
def add_product():
    form = AddProductForm()
    form.category.choices = [(category.id, category.name) for category in ProductCategory.query.all()]
    if not current_user.is_authenticated or current_user.role != 'admin':
        return redirect(url_for("/404"))

    if form.validate_on_submit():
        new_product = Product(name=form.name.data, price=form.price.data, img=form.img.data.filename,
                              category_id=form.category.data)

        db.session.add(new_product)
        db.session.commit()

        file_directory = path.join(app.root_path, "static", form.img.data.filename)
        form.img.data.save(file_directory)
        return redirect(url_for('index'))
    return render_template("add_product.html", form=form, )


@app.route("/edit_product/<int:product_id>", methods=["POST", "GET"])
def edit_product(product_id):
    chosen_product = Product.query.get(product_id)
    if not chosen_product:
        return render_template("404.html")

    if not current_user.is_authenticated or current_user.role != 'admin':
        return redirect(url_for("/404"))
    form = EditProductForm()
    form.category.choices = [(category.id, category.name) for category in ProductCategory.query.all()]

    if form.validate_on_submit():
        chosen_product.name = form.name.data
        chosen_product.price = form.price.data
        chosen_product.img = form.img.data.filename
        chosen_product.category = form.category.data

        db.session.commit()

        return redirect(url_for('index'))

    form.name.data = chosen_product.name
    form.price.data = chosen_product.price
    form.img.data = chosen_product.img
    form.category.data = chosen_product.category_id

    return render_template("edit_product.html", form=form, product=chosen_product)


@app.route("/delete_product/<int:product_id>")
def delete_product(product_id):
    if not current_user.is_authenticated or current_user.role != 'admin':
        return redirect(url_for("page_not_found"))

    chosen_product = Product.query.get(product_id)
    if not chosen_product:
        return render_template("404.html")

    db.session.delete(chosen_product)
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password_hash(form.password.data):
            login_user(user)

            return redirect(url_for("index"))
        else:
            return render_template("login.html", form=form, error="username or password specified incorrectly")

    return render_template("login.html", form=form)


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    existing_user = User.query.filter_by(username=form.username.data).first()
    if existing_user:
        flash('a user with the same name is already registered.', 'danger')
        return render_template("register.html", form=form)

    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template("register.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/404")
def page_not_found():
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
