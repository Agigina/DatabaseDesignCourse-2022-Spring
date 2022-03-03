from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, FloatField,IntegerField
from wtforms.validators import DataRequired, Email, Length, Optional, URL, EqualTo, Regexp

class ProfileForm(FlaskForm):
    # change BasicInfo
    nickname = StringField('Nickname', validators=[DataRequired(), Length(1, 64)])
    github = StringField('GitHub', validators=[Optional(), URL(), Length(0, 128)])
    website = StringField('Website', validators=[Optional(), URL(), Length(0, 128)])
    bio = TextAreaField('Bio', validators=[Optional(), Length(0, 120)])


class LoginForm(FlaskForm):
    phone = StringField('Phone', validators=[DataRequired(),Regexp(r"/^(?:(?:\+|00)86)?1(?:(?:3[\d])|(?:4[5-7|9])|(?:5[0-3|5-9])|(?:6[5-7])|(?:7[0-8])|(?:8[\d])|(?:9[1|8|9]))\d{8}$/",message="Incorrect phone number") ])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 64)])
    phone = StringField('Phone', validators=[DataRequired(),Regexp(r"/^(?:(?:\+|00)86)?1(?:(?:3[\d])|(?:4[5-7|9])|(?:5[0-3|5-9])|(?:6[5-7])|(?:7[0-8])|(?:8[\d])|(?:9[1|8|9]))\d{8}$/",message="Incorrect phone number") ])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6), EqualTo('password2')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    IDCard= StringField('IDCard', validators=[DataRequired(), Regexp(r'/^\d{6}(18|19|20)\d{2}(0\d|10|11|12)([0-2]\d|30|31)\d{3}(\d|X|x)$/')])
    UserType=BooleanField('Are u a worker')
    submit = SubmitField('Submit')

class JobForm(FlaskForm):
    # for job establish and job edition
    JName = StringField('Name', validators=[DataRequired(), Length(1, 1024)])
    salary=FloatField('Salary')
    Jcategory=StringField('Job category', validators=[DataRequired(), Length(1, 2048)])
    Jinformation=TextAreaField('Detailed Information', validators=[DataRequired(), Length(0, 120)])
    Jexperience=IntegerField('least work year',validators=[DataRequired()])
    submit=SubmitField('Submit')

class CompanyForm(FlaskForm):
    # for register a company and edit a company file
    CName = StringField('Name', validators=[DataRequired(), Length(1, 1024)])
    Corporate = StringField('Name', validators=[Length(1, 1024)])
    Cphone = StringField('Phone', validators=[DataRequired(),Regexp(r"/^(?:(?:\+|00)86)?1(?:(?:3[\d])|(?:4[5-7|9])|(?:5[0-3|5-9])|(?:6[5-7])|(?:7[0-8])|(?:8[\d])|(?:9[1|8|9]))\d{8}$/",message="Incorrect phone number") ])
    CInofrmation=TextAreaField('Detailed Information', validators=[DataRequired(), Length(0, 120)])
    submit=SubmitField('Submit')

class ProjectForm(FlaskForm):
    # for establish a project and edit a project file
    PName = StringField('Name', validators=[DataRequired(), Length(1, 1024)])
    PAddress=TextAreaField('Address', validators=[DataRequired(), Length(0, 120)])
    submit=SubmitField('Submit')