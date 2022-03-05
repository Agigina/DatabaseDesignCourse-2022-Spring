from flask import render_template, flash, redirect, url_for, Blueprint, request
from flask_login import login_user, logout_user, login_required, current_user

from InfoPlatform.forms import LoginForm
from InfoPlatform.models import Candidate, CompanyManager, ProjectManager, BasicInfo
from InfoPlatform.utils import redirect_back

anonymous_bp = Blueprint('anonymous', __name__)


@anonymous_bp.route('/', methods=['GET', 'POST'])
def login():
    # # return "a"
    # if current_user.is_authenticated:
    #     # 分类返回
    #     return redirect(url_for('candidate'))

    form = LoginForm()
    # if form.validate_on_submit():
    #     phone = form.phone.data
    #     password = form.password.data
    #     remember = form.remember.data
    #     admin = BasicInfo.query.filter(BasicInfo.Bphone == phone).first()
    #     if admin:
    #         if admin.Password == password:
    #             login_user(admin, remember)
    #             if admin.PMID:
    #                 return redirect(url_for('projectManager'))
    #             elif admin.CMID:
    #                 return redirect(url_for('companyManager'))
    #             elif admin.CAID:
    #                 return redirect(url_for('candidate'))
    #             return redirect_back()
    #         flash('账号或密码不正确', 'warning')
    #     else:
    #         flash('账户不存在，请注册。', 'warning')
    return render_template("anonymous/login_form.html",form=form)


@anonymous_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('candidate'))

    if request.method == 'POST':
        phone = request.form['phone'].lower()

        user = BasicInfo.query.filter_by(BasicInfo.Bphone == phone).first()
        if user is not None:
            flash('该手机号码已注册，请直接登录。')
            return redirect(url_for('/'))

        password = request.form['pass']
        password1 = request.form['cpass']
        if password != password1:
            flash('两次密码不一致，请重新输入')
            return redirect(url_for('/register'))

        user = User(nickname=nickname, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('chat.profile'))

    return render_template("anonymous/register.html")
