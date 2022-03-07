from flask import render_template, flash, redirect, request, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user

from InfoPlatform.forms import LoginForm
from InfoPlatform.models import Candidate
from InfoPlatform.utils import redirect_back
import datetime

candidate_bp = Blueprint('candidate', __name__)

@candidate_bp.route('/home', methods=['GET', 'POST'])
def home():
    # if current_user.is_authenticated:
    if True:
        applying_list=[]
        # 这个直接查询applying表
        available_job=[]

        if request.method == 'POST':
            search_name = request.form['search_name']
            print(search_name)
        today=datetime.date.today()
        time_str=str(today.year)+"年"+str(today.month)+"月"+str(today.day)+"日"
        recruiting=12

        
    # 按照时间顺序排序，查询job

    # 要传递的信息：当前时间；收到的offer；等待中的offer；
    # 各个工作：起止时间；工作名称；项目名称；工种；详细信息；投递截止日期。
    # 右上角个人信息：姓名/头像——要可以重定向到profile界面
    # 带通过工作：图像；申请时间；详细信息

    # 要返回的信息：通过左栏重定向：边栏可以切换排序规则：按照时间排序；按照项目名称排序；按照工作名称排序
    # 搜索信息：按照关键字搜索。
        return render_template("candidate/base.html",time=time_str,recruiting=recruiting)
    else:
        return render_template("error/LogInFirst.html")


@candidate_bp.route('/orderBYproject', methods=['GET', 'POST'])
def home_1():
    return render_template("candidate/base1.html")

@candidate_bp.route('/orderBYname', methods=['GET', 'POST'])
def home_2():
    return render_template("candidate/base2.html")
