from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields import StringField, IntegerField, SubmitField, PasswordField, DateField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, length, equal_to


class AddProductForm(FlaskForm):
    name = StringField("პროდუქტის სახელი", validators=[DataRequired(message="პროდუქტის სახელი არაა შეყვანილი")])
    price = IntegerField("ფასი", validators=[DataRequired(message="ფასი არაა მითითებული")])
    img = FileField("სურათი",
                    validators=[
                        DataRequired(),
                        FileAllowed(["jpg", "jpeg", "img", "png"], message="მხოლოდ jpg, jpeg, img ფაილები")
                    ])
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    submit = SubmitField("დამატება")


class RegisterForm(FlaskForm):
    username = StringField("სახელი", validators=[DataRequired(message="Username-ის შეყვანა აუცილებელია")])
    password = PasswordField("პაროლი", validators=[DataRequired(message="პაროლის შეყვანა აუცილებელია"),
                                                   length(min=8, max=64,
                                                          message="პაროლის ზომა მინიმუმ 8 სიმბოლო, მაქსიმუმ 64")])
    confirm_password = PasswordField("გაიმეორეთ პაროლი",
                                     validators=[DataRequired(), equal_to("password", message="პაროლები არ ემთხვევა")])
    birthday = DateField("მიუთითეთ დაბადების თარიღი",
                         validators=[DataRequired(message="დაბადების თარიღი არაა მითითებული")])
    submit = SubmitField("რეგისტრაცია")


class LoginForm(FlaskForm):
    username = StringField("სახელი", validators=[DataRequired(message="Username-ის შეყვანა აუცილებელია")])
    password = PasswordField("პაროლი", validators=[DataRequired(message="პაროლის შეყვანა აუცილებელია")])
    submit = SubmitField("ავტორიზაცია")


class EditProductForm(FlaskForm):
    name = StringField("პროდუქტის სახელი", validators=[DataRequired(message="პროდუქტის სახელი არაა შეყვანილი")])
    price = IntegerField("ფასი", validators=[DataRequired(message="ფასი არაა მითითებული")])
    img = FileField("სურათი",
                    validators=[
                        FileAllowed(["jpg", "jpeg", "img", "png"], message="მხოლოდ jpg, jpeg, img, png ფაილები")
                    ])
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    submit = SubmitField("შეცვლა")
