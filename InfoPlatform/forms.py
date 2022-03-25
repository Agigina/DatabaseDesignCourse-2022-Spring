from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField,SubmitField, TextAreaField, PasswordField, BooleanField, FloatField, IntegerField
from flask_wtf.file import FileAllowed,FileField
from flask_uploads import UploadSet, IMAGES
from wtforms.validators import DataRequired, Email, Length,EqualTo, Regexp, InputRequired

photos = UploadSet('photos', IMAGES)
class ProfileForm(FlaskForm):
    # change BasicInfo
    nickname = StringField('Nickname',
                           render_kw={'placeholder': "姓名",
                                      "class": "form-control"},
                           validators=[
                               DataRequired(), Length(1, 64)])
    gender = SelectField(
        label='类别',
        validators=[DataRequired('请选择标签')],
        render_kw={
            'placeholder': "姓名", 'class': 'form-control selectpicker'
        },
        choices=[('1', '男'), (2, '女'), (3, '不愿透露')],
        default=3,
        coerce=int
    )
    email = StringField('Email',
                        render_kw={'placeholder': "电子邮箱（可选）",
                                   "class": "form-control"},
                        validators=[Email()])
    phone = StringField('Phone',
                        render_kw={'placeholder': "手机号码",
                                   "class": "form-control"},
                        validators=[InputRequired(), DataRequired(),
                                    Regexp(
                            r"^1(3\d|4[4-9]|5[0-35-9]|6[67]|7[013-8]|8[0-9]|9[0-9])\d{8}$",
                            message="Incorrect phone number")])
    IDCard = StringField('IDCard',
                         render_kw={'placeholder': "身份证号",
                                    "class": "form-control"},
                         validators=[DataRequired(), Regexp(
                             r'/^[1-9]\d{7}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}$|^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$')])
    Address = StringField('Name',
                          render_kw={'placeholder': "地址", "class": "form-control"})

    cate = StringField('Category',
                           render_kw={'placeholder': "工种",
                                      "class": "form-control"},
                           validators=[
                               DataRequired(), Length(1, 64)])
    portrait=FileField('portrait',validators=[FileAllowed(photos,'Images only!')])
    health=FileField('health',validators=[FileAllowed(photos,'Images only!')])
    certificate=FileField('certificate',validators=[FileAllowed(photos,'Images only!')])
    inform = StringField('inform',
                           render_kw={'placeholder': "经历",
                                      "class": "form-control"},
                           validators=[
                                Length(1, 64)])
    experience = StringField('experience',
                           render_kw={'placeholder': "备注",
                                      "class": "form-control"},
                           validators=[
                                Length(1, 64)])

    status = RadioField('status', choices = [(0,'空闲'),(1,'忙')])
    experin=IntegerField('工作年限', validators=[DataRequired()])

class cmProfileForm(FlaskForm):
    # change BasicInfo
    nickname = StringField('Nickname',
                           render_kw={'placeholder': "姓名",
                                      "class": "form-control"},
                           validators=[
                               DataRequired(), Length(1, 64)])
    gender = SelectField(
        label='类别',
        validators=[DataRequired('请选择标签')],
        render_kw={
            'placeholder': "姓名", 'class': 'form-control selectpicker'
        },
        choices=[('1', '男'), (2, '女'), (3, '不愿透露')],
        default=3,
        coerce=int
    )
    portrait=FileField('portrait',validators=[FileAllowed(photos,'Images only!')])

    email = StringField('Email',
                        render_kw={'placeholder': "电子邮箱（可选）",
                                   "class": "form-control"},
                        validators=[Email()])
    phone = StringField('Phone',
                        render_kw={'placeholder': "手机号码",
                                   "class": "form-control"},
                        validators=[InputRequired(), DataRequired(),
                                    Regexp(
                            r"^1(3\d|4[4-9]|5[0-35-9]|6[67]|7[013-8]|8[0-9]|9[0-9])\d{8}$",
                            message="Incorrect phone number")])
    IDCard = StringField('IDCard',
                         render_kw={'placeholder': "身份证号",
                                    "class": "form-control"},
                         validators=[DataRequired(), Regexp(
                             r'/^[1-9]\d{7}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}$|^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$')])
    Address = StringField('Name',
                          render_kw={'placeholder': "地址", "class": "form-control"})

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
                        render_kw={'placeholder': "手机号码",
                                   "type": "text", "required": "required"},
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
                        validators=[Email()])
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
