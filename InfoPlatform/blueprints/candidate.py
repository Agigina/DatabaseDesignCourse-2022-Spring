from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user

from InfoPlatform.forms import LoginForm
from InfoPlatform.models import Candidate
from InfoPlatform.utils import redirect_back

candidate_bp = Blueprint('candidate', __name__)

@candidate_bp.route('/login', methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('blog.index'))

    # form = LoginForm()
    # if form.validate_on_submit():
    #     username = form.username.data
    #     password = form.password.data
    #     remember = form.remember.data
    #     admin = Candidate.query.first()
    #     if admin:
    #         if username == admin.username and admin.validate_password(password):
    #             login_user(admin, remember)
    #             flash('Welcome back.', 'info')
    #             return redirect_back()
    #         flash('Invalid username or password.', 'warning')
    #     else:
    #         flash('No account.', 'warning')
    return render_template('candidate/login.html', form=form)