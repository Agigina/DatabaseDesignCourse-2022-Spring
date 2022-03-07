from flask import render_template, flash, redirect, url_for, Blueprint, request
from flask_login import login_user, logout_user, login_required, current_user

from InfoPlatform.forms import LoginForm, RegisterForm
from InfoPlatform.models import Candidate, BasicInfo
from InfoPlatform.utils import redirect_back
from InfoPlatform import db
anonymous_bp = Blueprint('anonymous', __name__)

@anonymous_bp.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        phone = form.phone.data
        password = form.password.data
        # remember = form.remember.data
        admin = BasicInfo.query.filter(BasicInfo.Bphone == phone).first()
        if admin:
            print(admin)
            if admin.Password == password:
                login_user(admin)
                if admin.UserType==1:
                    return redirect(url_for('candidate.home'))
                elif admin.UserType==0:
                    return redirect(url_for('companyManager'))
                return redirect_back()
            flash('账号或密码不正确', 'warning')
        else:
            print("no")
            flash('账户不存在，请注册。', 'warning')
    else:
        print("invalid")
    return render_template("anonymous/login_form.html", form=form)


@anonymous_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    print(form.data)
    # if current_user.is_authenticated:
    #     return "a"
        # return redirect(url_for('candidate'))
    if form.validate_on_submit():
        phone=form.phone.data
        user = BasicInfo.query.filter(BasicInfo.Bphone == phone).first()
        if user is not None:
            print(2)
            flash('该手机号码已注册，请直接登录。')
            # js2py.eval_js("alert('该手机号码已注册，请直接登录。');")
            # return "redirect(url_for('/'))"
            return login()

        password = form.password
        if password != form.password2:
            print(1)
            # js2py.eval_js("alert('两次密码不一致，请重新输入')")
            flash('两次密码不一致，请重新输入')
            return redirect(url_for('/register'))
        name=form.fname.data+form.lname.data
        new_user = BasicInfo(BName=name, Bphone=phone,
                      IDCard=form.IDCard.data, UserType=0, Password=form.password.data, Bemail=form.email.data)
        db.session.add(new_user)
        new_candidate=Candidate()
        new_candidate.basic_info=new_user
        db.session.add(new_candidate)
        db.session.commit()
        login_user(new_user)
        # js2py.eval_js("alert('注册成功')")
        # return redirect(url_for('/'))
        return redirect(url_for('candidate.home'))
    else:
        print(form.email.errors,form.email.data) 
        print(form.fname.errors,form.fname.data) 
        print(form.lname.errors,form.lname.data) 
        print(form.phone.errors,form.phone.data) 
        print(form.IDCard.errors,form.IDCard.data) 
        print(form.password.errors,form.password.data) 
        print(form.password2.errors,form.password2.data) 
        print(form.Address.errors,form.Address.data) 
    return render_template("anonymous/register_form1.html", form=form)
