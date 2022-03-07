from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user

from InfoPlatform.forms import LoginForm
from InfoPlatform.models import Candidate
from InfoPlatform.utils import redirect_back

candidate_bp = Blueprint('candidate', __name__)

@candidate_bp.route('/', methods=['GET', 'POST'])
def home():
    # 要传递的信息：当前时间；收到的offer；等待中的offer；
    # 各个工作：起止时间；工作名称；项目名称；工种；详细信息；投递截止日期。
    # 右上角个人信息：姓名/头像——要可以重定向到profile界面‘
    # 带通过工作：图像；申请时间；详细信息

    # 要返回的信息：通过左栏重定向：边栏可以切换排序规则：按照时间排序；按照项目名称排序；按照工作名称排序
    # 搜索信息：按照关键字搜索。
    return render_template("candidate/base.html")
