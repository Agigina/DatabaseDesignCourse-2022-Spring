from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, FloatField, IntegerField
from wtforms.validators import DataRequired, Email, Length, Optional, URL, EqualTo, Regexp, InputRequired


class ProfileForm(FlaskForm):
    # change BasicInfo
    nickname = StringField('Nickname', validators=[
                           DataRequired(), Length(1, 64)])
    github = StringField('GitHub', validators=[
                         Optional(), URL(), Length(0, 128)])
    website = StringField('Website', validators=[
                          Optional(), URL(), Length(0, 128)])
    bio = TextAreaField('Bio', validators=[Optional(), Length(0, 120)])


class LoginForm(FlaskForm):
    phone = StringField('Phone',
                        render_kw={'placeholder': "手机号码"},
                        validators=[InputRequired(), DataRequired(),
                                    Regexp(
                            r"^1(3\d|4[4-9]|5[0-35-9]|6[67]|7[013-8]|8[0-9]|9[0-9])\d{8}$",
                            message="Incorrect phone number")])
    password = PasswordField('Password',
                             render_kw={'placeholder': "密码"},
                             validators=[DataRequired()])
    submit = SubmitField('登陆')


class RegisterForm(FlaskForm):
    fname = StringField('Name',
                        render_kw={'placeholder': "姓氏"},
                        validators=[DataRequired(), Length(1, 64)])
    lname = StringField('Name',
                        render_kw={'placeholder': "名"},
                        validators=[DataRequired(), Length(1, 64)])
    Address = StringField('Name',
                          render_kw={'placeholder': "地址"})
    phone = StringField('Phone',
                        render_kw={'placeholder': "手机号码"},
                        validators=[InputRequired(), DataRequired(), Regexp(
                            r"^1(3\d|4[4-9]|5[0-35-9]|6[67]|7[013-8]|8[0-9]|9[0-9])\d{8}$", message="Incorrect phone number")])
    password = PasswordField('Password',
                             render_kw={'placeholder': "密码"},
                             validators=[
                                 DataRequired(), Length(min=6), EqualTo('password2')])
    password2 = PasswordField('Confirm Password',
                              render_kw={'placeholder': "确认密码"},
                              validators=[DataRequired()])
    IDCard = StringField('IDCard',
                         render_kw={'placeholder': "身份证号"},
                         validators=[DataRequired(), Regexp(
                             r'/^[1-9]\d{7}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}$|^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$')])
    # UserType=BooleanField('Are u a worker')
    email = StringField('Email',
                        render_kw={'placeholder': "电子邮箱（可选）"},
                        validators=[Email(), Length(1, 254)])
    submit = SubmitField('Submit')


class JobForm(FlaskForm):
    # for job establish and job edition
    JName = StringField('Name', validators=[DataRequired(), Length(1, 1024)])
    salary = FloatField('Salary')
    Jcategory = StringField('Job category', validators=[
                            DataRequired(), Length(1, 2048)])
    Jinformation = TextAreaField('Detailed Information', validators=[
                                 DataRequired(), Length(0, 120)])
    Jexperience = IntegerField('least work year', validators=[DataRequired()])
    submit = SubmitField('Submit')


class CompanyForm(FlaskForm):
    # for register a company and edit a company file
    CName = StringField('Name', validators=[DataRequired(), Length(1, 1024)])
    Corporate = StringField('Name', validators=[Length(1, 1024)])
    Cphone = StringField('Phone', validators=[DataRequired(), Regexp(
        r"/^(?:(?:\+|00)86)?1(?:(?:3[\d])|(?:4[5-7|9])|(?:5[0-3|5-9])|(?:6[5-7])|(?:7[0-8])|(?:8[\d])|(?:9[1|8|9]))\d{8}$/", message="Incorrect phone number")])
    CInofrmation = TextAreaField('Detailed Information', validators=[
                                 DataRequired(), Length(0, 120)])
    submit = SubmitField('Submit')


class ProjectForm(FlaskForm):
    # for establish a project and edit a project file
    PName = StringField('Name', validators=[DataRequired(), Length(1, 1024)])
    PAddress = TextAreaField('Address', validators=[
                             DataRequired(), Length(0, 120)])
    submit = SubmitField('Submit')