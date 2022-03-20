from flask import render_template, flash, redirect, request, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user

from InfoPlatform.forms import ProfileForm
from InfoPlatform.models import Candidate, BasicInfo, Company, Project, Jobs, Applying
from InfoPlatform.utils import redirect_back
import datetime

candidate_bp = Blueprint('candidate', __name__)

color_map=[["#fee4cb","#ff942e"],["#e9e7fd","#4f3ff0"],["#dbf6fd","#096c86"],["#ffd3e2","#df3670"],
["#c8f7dc","#34c471"],["#d5deff","#4067f9"],["#F6EEE0","#E4B7A0"],["#FADCD9","#F79489"],["#ECE3F0","#D3BBDD"]
]

# 详情界面
# 投递键
# profile

@candidate_bp.route('/home', methods=['GET', 'POST'])
def home():
    # print(current_user)
    if current_user.is_authenticated:
        applying_list = []
        # 这个直接查询applying表
        available_job = []
        applies = Applying.query.filter(
            Applying.CAID == current_user.get_id()).all()
        
        waiting_num=0
        offer_num=0
        for item in applies:
            job = Jobs.query.filter(Jobs.JID == item.JID).first()
            proj = Project.query.filter(Project.PID == job.PID).first()
            apply_time = "申请时间："+str(item.applytime.date())
            status_now = "等待中" if item.status == 0 else "通过" if item.status == 1 else "拒绝"
            if item.status==0: 
                waiting_num+=1
            elif item.status==1:
                offer_num+=1
            applying_list.append({"applytime": apply_time, "status": status_now, "proj_name": proj.PName,
                                 "job_name": job.Jname, "Info": "类型："+str(job.Jcategory)+"，信息："+str(job.Jinformation),
                                  "PPortrait": proj.PPortrait.decode('ascii')})

        if request.method == 'POST':
            search_name = request.form['search_name']
            print(search_name)
            jobs = Jobs.query.filter(Jobs.Jname.like("%"+search_name+"%")).all()
            for i, item in enumerate(jobs):
                proj = Project.query.filter(Project.PID == item.PID).first()
                if i>=len(color_map):
                    i-=len(color_map)
                progress=(datetime.datetime.now()-item.JBegin).days/(item.JFinal-item.JBegin).days
                progress=0 if progress<0 else progress
                available_job.append(
                    {"JBegin": str(item.JBegin.date()), "JFinal": str(item.JFinal.date()), "Jname": item.Jname, "proj_name": proj.PName,
                     "Jinformation": item.Jinformation, "Jddl": (item.Jddl-datetime.datetime.now()).days,
                     "thin":color_map[i][0],"thick":color_map[i][1],"proj_port":proj.PPortrait.decode('ascii'),
                     "progress_str":"%.2f%%" % (progress * 100)})
        else:
            jobs = Jobs.query.all()
            for i, item in enumerate(jobs):
                proj = Project.query.filter(Project.PID == item.PID).first()
                if i>=len(color_map):
                    i-=len(color_map)
                progress=(datetime.datetime.now()-item.JBegin).days/(item.JFinal-item.JBegin).days
                progress=0 if progress<0 else progress
                available_job.append(
                    {"JBegin": str(item.JBegin.date()), "JFinal": str(item.JFinal.date()), "Jname": item.Jname, "proj_name": proj.PName,
                     "Jinformation": item.Jinformation, "Jddl": (item.Jddl-datetime.datetime.now()).days,
                     "thin":color_map[i][0],"thick":color_map[i][1],"proj_port":proj.PPortrait.decode('ascii'),
                     "progress_str":"%.2f%%" % (progress * 100)})
        today = datetime.date.today()
        time_str = str(today.year)+"年"+str(today.month)+"月"+str(today.day)+"日"
        recruiting = Jobs.query.count()

        user_info = Candidate.query.filter(
            Candidate.CAID == current_user.get_id()).first()
        basic_info = BasicInfo.query.filter(
            Candidate.id == user_info.id).first()
        portrait = basic_info.BPortrait.decode('ascii')
        return render_template("candidate/base.html", time=time_str, recruiting=recruiting, 
                                img=portrait, name=basic_info.BName, applying_list=applying_list, 
                                available_job=available_job,waiting_num=waiting_num,offer_num=offer_num)
    else:
        return render_template("error/LogInFirst.html")


@candidate_bp.route('/orderBYproject', methods=['GET', 'POST'])
def home_1():
    if current_user.is_authenticated:
        applying_list = []
        # 这个直接查询applying表
        available_job = []
        applies = Applying.query.filter(
            Applying.CAID == current_user.get_id()).all()
        
        waiting_num=0
        offer_num=0
        for item in applies:
            job = Jobs.query.filter(Jobs.JID == item.JID).first()
            proj = Project.query.filter(Project.PID == job.PID).first()
            apply_time = "申请时间："+str(item.applytime.date())
            status_now = "等待中" if item.status == 0 else "通过" if item.status == 1 else "拒绝"
            if item.status==0: 
                waiting_num+=1
            elif item.status==1:
                offer_num+=1
            applying_list.append({"applytime": apply_time, "status": status_now, "proj_name": proj.PName,
                                 "job_name": job.Jname, "Info": "类型："+str(job.Jcategory)+"，信息："+str(job.Jinformation),
                                  "PPortrait": proj.PPortrait.decode('ascii')})

        if request.method == 'POST':
            search_name = request.form['search_name']
            print(search_name)
            jobs = Jobs.query.filter(Jobs.Jname.like("%"+search_name+"%")).all()
            for i, item in enumerate(jobs):
                proj = Project.query.filter(Project.PID == item.PID).first()
                if i>=len(color_map):
                    i-=len(color_map)
                progress=(datetime.datetime.now()-item.JBegin).days/(item.JFinal-item.JBegin).days
                progress=0 if progress<0 else progress
                available_job.append(
                    {"JBegin": str(item.JBegin.date()), "JFinal": str(item.JFinal.date()), "Jname": item.Jname, "proj_name": proj.PName,
                     "Jinformation": item.Jinformation, "Jddl": (item.Jddl-datetime.datetime.now()).days,
                     "thin":color_map[i][0],"thick":color_map[i][1],"proj_port":proj.PPortrait.decode('ascii'),
                     "progress_str":"%.2f%%" % (progress * 100)})
        else: 
            jobs = Jobs.query.order_by(Jobs.JBegin).all()
            for i, item in enumerate(jobs):
                proj = Project.query.filter(Project.PID == item.PID).first()
                if i>=len(color_map):
                    i-=len(color_map)
                progress=(datetime.datetime.now()-item.JBegin).days/(item.JFinal-item.JBegin).days
                progress=0 if progress<0 else progress
                available_job.append(
                    {"JBegin": str(item.JBegin.date()), "JFinal": str(item.JFinal.date()), "Jname": item.Jname, "proj_name": proj.PName,
                     "Jinformation": item.Jinformation, "Jddl": (item.Jddl-datetime.datetime.now()).days,
                     "thin":color_map[i][0],"thick":color_map[i][1],"proj_port":proj.PPortrait.decode('ascii'),
                     "progress_str":"%.2f%%" % (progress * 100)})
        today = datetime.date.today()
        time_str = str(today.year)+"年"+str(today.month)+"月"+str(today.day)+"日"
        recruiting = Jobs.query.count()

        user_info = Candidate.query.filter(
            Candidate.CAID == current_user.get_id()).first()
        basic_info = BasicInfo.query.filter(
            Candidate.id == user_info.id).first()
        portrait = basic_info.BPortrait.decode('ascii')
        return render_template("candidate/base1.html", time=time_str, recruiting=recruiting, 
                                img=portrait, name=basic_info.BName, applying_list=applying_list, 
                                available_job=available_job,waiting_num=waiting_num,offer_num=offer_num)
    else:
        return render_template("error/LogInFirst.html")


@candidate_bp.route('/orderBYname', methods=['GET', 'POST'])
def home_2():
    if current_user.is_authenticated:
        applying_list = []
        # 这个直接查询applying表
        available_job = []
        applies = Applying.query.filter(
            Applying.CAID == current_user.get_id()).all()
        
        waiting_num=0
        offer_num=0
        for item in applies:
            job = Jobs.query.filter(Jobs.JID == item.JID).first()
            proj = Project.query.filter(Project.PID == job.PID).first()
            apply_time = "申请时间："+str(item.applytime.date())
            status_now = "等待中" if item.status == 0 else "通过" if item.status == 1 else "拒绝"
            if item.status==0: 
                waiting_num+=1
            elif item.status==1:
                offer_num+=1
            applying_list.append({"applytime": apply_time, "status": status_now, "proj_name": proj.PName,
                                 "job_name": job.Jname, "Info": "类型："+str(job.Jcategory)+"，信息："+str(job.Jinformation),
                                  "PPortrait": proj.PPortrait.decode('ascii')})

        if request.method == 'POST':
            search_name = request.form['search_name']
            print(search_name)
            jobs = Jobs.query.filter(Jobs.Jname.like("%"+search_name+"%")).all()
            for i, item in enumerate(jobs):
                proj = Project.query.filter(Project.PID == item.PID).first()
                if i>=len(color_map):
                    i-=len(color_map)
                progress=(datetime.datetime.now()-item.JBegin).days/(item.JFinal-item.JBegin).days
                progress=0 if progress<0 else progress
                available_job.append(
                    {"JBegin": str(item.JBegin.date()), "JFinal": str(item.JFinal.date()), "Jname": item.Jname, "proj_name": proj.PName,
                     "Jinformation": item.Jinformation, "Jddl": (item.Jddl-datetime.datetime.now()).days,
                     "thin":color_map[i][0],"thick":color_map[i][1],"proj_port":proj.PPortrait.decode('ascii'),
                     "progress_str":"%.2f%%" % (progress * 100)})
        else:
            jobs = Jobs.query.order_by(Jobs.Jddl).all()
            for i, item in enumerate(jobs):
                proj = Project.query.filter(Project.PID == item.PID).first()
                if i>=len(color_map):
                    i-=len(color_map)
                progress=(datetime.datetime.now()-item.JBegin).days/(item.JFinal-item.JBegin).days
                progress=0 if progress<0 else progress
                available_job.append(
                    {"JBegin": str(item.JBegin.date()), "JFinal": str(item.JFinal.date()), "Jname": item.Jname, "proj_name": proj.PName,
                     "Jinformation": item.Jinformation, "Jddl": (item.Jddl-datetime.datetime.now()).days,
                     "thin":color_map[i][0],"thick":color_map[i][1],"proj_port":proj.PPortrait.decode('ascii'),
                     "progress_str":"%.2f%%" % (progress * 100)})
        today = datetime.date.today()
        time_str = str(today.year)+"年"+str(today.month)+"月"+str(today.day)+"日"
        recruiting = Jobs.query.count()

        user_info = Candidate.query.filter(
            Candidate.CAID == current_user.get_id()).first()
        basic_info = BasicInfo.query.filter(
            Candidate.id == user_info.id).first()
        portrait = basic_info.BPortrait.decode('ascii')
        return render_template("candidate/base2.html", time=time_str, recruiting=recruiting, 
                                img=portrait, name=basic_info.BName, applying_list=applying_list, 
                                available_job=available_job,waiting_num=waiting_num,offer_num=offer_num)
    else:
        return render_template("error/LogInFirst.html")

@candidate_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        print(form.data)
    else:
        print(form.errors)
    return render_template("candidate/profile.html",form=form)