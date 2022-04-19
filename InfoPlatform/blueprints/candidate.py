from asyncio.windows_events import NULL
from flask import render_template, flash, redirect, request, url_for, Blueprint
from flask_login import current_user

from InfoPlatform.forms import ProfileForm
from InfoPlatform.models import Candidate, BasicInfo, Project, Jobs, Applying
import datetime
from flask_uploads import UploadSet, IMAGES

import os
from InfoPlatform.extensions import db

candidate_bp = Blueprint('candidate', __name__)
photos = UploadSet('photos', IMAGES)
color_map = [["#fee4cb", "#ff942e"], ["#e9e7fd", "#4f3ff0"], ["#dbf6fd", "#096c86"], ["#ffd3e2", "#df3670"],
             ["#c8f7dc", "#34c471"], ["#d5deff", "#4067f9"], ["#F6EEE0",
                                                              "#E4B7A0"], ["#FADCD9", "#F79489"], ["#ECE3F0", "#D3BBDD"]
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

        waiting_num = 0
        offer_num = 0
        for item in applies:
            job = Jobs.query.filter(Jobs.JID == item.JID).first()
            proj = Project.query.filter(Project.PID == job.PID).first()
            apply_time = "申请时间："+str(item.applytime.date())
            status_now = "等待中" if item.status == 0 else "通过" if item.status == 1 else "拒绝"
            if item.status == 0:
                waiting_num += 1
            elif item.status == 1:
                offer_num += 1
            applying_list.append({"applytime": apply_time, "status": status_now, "proj_name": proj.PName,
                                 "job_name": job.Jname, "Info": "类型："+str(job.Jcategory)+"，信息："+str(job.Jinformation),
                                  "PPortrait": proj.PPortrait.decode('ascii'),"APID":item.APID})

        if request.method == 'POST':
            search_name = request.form['search_name']
            print(search_name)
            jobs = Jobs.query.filter(
                Jobs.Jname.like("%"+search_name+"%")).all()
            for i, item in enumerate(jobs):
                proj = Project.query.filter(Project.PID == item.PID).first()
                if i >= len(color_map):
                    i -= len(color_map)
                progress = (datetime.datetime.now()-item.JBegin).days / \
                    (item.JFinal-item.JBegin).days
                progress = 0 if progress < 0 else progress
                available_job.append(
                    {"JBegin": str(item.JBegin.date()), "JFinal": str(item.JFinal.date()), "Jname": item.Jname, "proj_name": proj.PName,
                     "Jinformation": item.Jinformation, "Jddl": (item.Jddl-datetime.datetime.now()).days,
                     "thin": color_map[i][0], "thick": color_map[i][1], "proj_port": proj.PPortrait.decode('ascii'),
                     "progress_str": "%.2f%%" % (progress * 100),"JID":item.JID})
        else:
            jobs = Jobs.query.all()
            for i, item in enumerate(jobs):
                proj = Project.query.filter(Project.PID == item.PID).first()
                if i >= len(color_map):
                    i -= len(color_map)
                progress = (datetime.datetime.now()-item.JBegin).days / \
                    (item.JFinal-item.JBegin).days
                progress = 0 if progress < 0 else progress
                available_job.append(
                    {"JBegin": str(item.JBegin.date()), "JFinal": str(item.JFinal.date()), "Jname": item.Jname, "proj_name": proj.PName,
                     "Jinformation": item.Jinformation, "Jddl": (item.Jddl-datetime.datetime.now()).days,
                     "thin": color_map[i][0], "thick": color_map[i][1], "proj_port": proj.PPortrait.decode('ascii'),
                     "progress_str": "%.2f%%" % (progress * 100),"JID":item.JID})
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
                               available_job=available_job, waiting_num=waiting_num, offer_num=offer_num)
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

        waiting_num = 0
        offer_num = 0
        for item in applies:
            job = Jobs.query.filter(Jobs.JID == item.JID).first()
            proj = Project.query.filter(Project.PID == job.PID).first()
            apply_time = "申请时间："+str(item.applytime.date())
            status_now = "等待中" if item.status == 0 else "通过" if item.status == 1 else "拒绝"
            if item.status == 0:
                waiting_num += 1
            elif item.status == 1:
                offer_num += 1
            applying_list.append({"applytime": apply_time, "status": status_now, "proj_name": proj.PName,
                                 "job_name": job.Jname, "Info": "类型："+str(job.Jcategory)+"，信息："+str(job.Jinformation),
                                  "PPortrait": proj.PPortrait.decode('ascii')})

        if request.method == 'POST':
            search_name = request.form['search_name']
            print(search_name)
            jobs = Jobs.query.filter(
                Jobs.Jname.like("%"+search_name+"%")).all()
            for i, item in enumerate(jobs):
                proj = Project.query.filter(Project.PID == item.PID).first()
                if i >= len(color_map):
                    i -= len(color_map)
                progress = (datetime.datetime.now()-item.JBegin).days / \
                    (item.JFinal-item.JBegin).days
                progress = 0 if progress < 0 else progress
                available_job.append(
                    {"JBegin": str(item.JBegin.date()), "JFinal": str(item.JFinal.date()), "Jname": item.Jname, "proj_name": proj.PName,
                     "Jinformation": item.Jinformation, "Jddl": (item.Jddl-datetime.datetime.now()).days,
                     "thin": color_map[i][0], "thick": color_map[i][1], "proj_port": proj.PPortrait.decode('ascii'),
                     "progress_str": "%.2f%%" % (progress * 100),"JID":item.JID})
        else:
            jobs = Jobs.query.order_by(Jobs.JBegin).all()
            for i, item in enumerate(jobs):
                proj = Project.query.filter(Project.PID == item.PID).first()
                if i >= len(color_map):
                    i -= len(color_map)
                progress = (datetime.datetime.now()-item.JBegin).days / \
                    (item.JFinal-item.JBegin).days
                progress = 0 if progress < 0 else progress
                available_job.append(
                    {"JBegin": str(item.JBegin.date()), "JFinal": str(item.JFinal.date()), "Jname": item.Jname, "proj_name": proj.PName,
                     "Jinformation": item.Jinformation, "Jddl": (item.Jddl-datetime.datetime.now()).days,
                     "thin": color_map[i][0], "thick": color_map[i][1], "proj_port": proj.PPortrait.decode('ascii'),
                     "progress_str": "%.2f%%" % (progress * 100),"JID":item.JID})
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
                               available_job=available_job, waiting_num=waiting_num, offer_num=offer_num)
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

        waiting_num = 0
        offer_num = 0
        for item in applies:
            job = Jobs.query.filter(Jobs.JID == item.JID).first()
            proj = Project.query.filter(Project.PID == job.PID).first()
            apply_time = "申请时间："+str(item.applytime.date())
            status_now = "等待中" if item.status == 0 else "通过" if item.status == 1 else "拒绝"
            if item.status == 0:
                waiting_num += 1
            elif item.status == 1:
                offer_num += 1
            applying_list.append({"applytime": apply_time, "status": status_now, "proj_name": proj.PName,
                                 "job_name": job.Jname, "Info": "类型："+str(job.Jcategory)+"，信息："+str(job.Jinformation),
                                  "PPortrait": proj.PPortrait.decode('ascii')})

        if request.method == 'POST':
            search_name = request.form['search_name']
            print(search_name)
            jobs = Jobs.query.filter(
                Jobs.Jname.like("%"+search_name+"%")).all()
            for i, item in enumerate(jobs):
                proj = Project.query.filter(Project.PID == item.PID).first()
                if i >= len(color_map):
                    i -= len(color_map)
                progress = (datetime.datetime.now()-item.JBegin).days / \
                    (item.JFinal-item.JBegin).days
                progress = 0 if progress < 0 else progress
                available_job.append(
                    {"JBegin": str(item.JBegin.date()), "JFinal": str(item.JFinal.date()), "Jname": item.Jname, "proj_name": proj.PName,
                     "Jinformation": item.Jinformation, "Jddl": (item.Jddl-datetime.datetime.now()).days,
                     "thin": color_map[i][0], "thick": color_map[i][1], "proj_port": proj.PPortrait.decode('ascii'),
                     "progress_str": "%.2f%%" % (progress * 100),"JID":item.JID})
        else:
            jobs = Jobs.query.order_by(Jobs.Jddl).all()
            for i, item in enumerate(jobs):
                proj = Project.query.filter(Project.PID == item.PID).first()
                if i >= len(color_map):
                    i -= len(color_map)
                progress = (datetime.datetime.now()-item.JBegin).days / \
                    (item.JFinal-item.JBegin).days
                progress = 0 if progress < 0 else progress
                available_job.append(
                    {"JBegin": str(item.JBegin.date()), "JFinal": str(item.JFinal.date()), "Jname": item.Jname, "proj_name": proj.PName,
                     "Jinformation": item.Jinformation, "Jddl": (item.Jddl-datetime.datetime.now()).days,
                     "thin": color_map[i][0], "thick": color_map[i][1], "proj_port": proj.PPortrait.decode('ascii'),
                     "progress_str": "%.2f%%" % (progress * 100),"JID":item.JID})
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
                               available_job=available_job, waiting_num=waiting_num, offer_num=offer_num)
    else:
        return render_template("error/LogInFirst.html")


@candidate_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if current_user.is_authenticated:
        form = ProfileForm()
        if form.validate_on_submit():
            import base64
            user = Candidate.query.filter(
                current_user.get_id() == Candidate.CAID).first()
            info = BasicInfo.query.filter(BasicInfo.id == user.id).first()
            print(info.BName)
            print(info)
            info.BName = form.nickname.data
            portrait=form.portrait.data.filename
            form.portrait.data.save(portrait)
            portrait1 = open(portrait, 'rb')
            portrait1 = base64.b64encode(portrait1.read())
            os.remove(portrait)
            info.BPortrait = portrait1
            info.Bphone = form.phone.data
            info.IDCard = form.IDCard.data
            info.Bemail = form.email.data
            info.BAddress = form.Address.data
            info.Bgender = form.gender.data
            user.Ccategory = form.cate.data
            if form.health.data:
                health=form.health.data.filename
                form.health.data.save(health)
                health1 = open(health, 'rb')
                health1 = base64.b64encode(health1.read())
                os.remove(health)
                user.health = health1
            user.Cexperience = form.experin.data
            user.detailExperience = form.experience.data
            user.status = False if form.status.data ==0 else True
            if form.certificate.data:
                certificate=form.certificate.data.filename
                form.certificate.data.save(certificate)
                certificate1 = open(certificate, 'rb')
                certificate1 = base64.b64encode(certificate1.read())
                os.remove(certificate)
                user.certification = certificate1
            user.moreInfo = form.inform.data

            print(info.BName,user.Cexperience)
            db.session.commit()
            return redirect(url_for('candidate.home'))
        else:
            print(form.errors)
        return render_template("candidate/profile.html", form=form)
    else:
        return render_template("error/LogInFirst.html")


@candidate_bp.route('/job-info/<id>', methods=['GET', 'POST'])
def info(id):
    if current_user.is_authenticated:
        job = Jobs.query.filter(
            id == Jobs.JID).first()
        # job name,job detail
        info=[]
        if job.salary:
            info.append("工资范围："+str(job.salary))
        if job.Jcategory:
            info.append("期望工种："+job.Jcategory)
        if job.Jexperience:
            info.append("最少工作年限："+job.Jexperience)
        info.append("详情信息："+job.Jinformation)
        
        return render_template("candidate/detail_info.html",info=info,name=job.Jname,id=id)
    else:
        return render_template("error/LogInFirst.html")


@candidate_bp.route('/job-apply/<id>', methods=['GET', 'POST'])
def apply(id):
    if current_user.is_authenticated:
        app=Applying.query.filter(
            Applying.CAID==current_user.get_id()
        ).filter(
            Applying.JID==id
        ).all()
        if app:
            return home()
        else:
            app1 = Applying(applytime=datetime.datetime.now(),status=int(0))
            job1 = Jobs.query.filter(
                id == Jobs.JID).first()
            job1.APID.append(app1)
            ca = Candidate.query.filter(
                current_user.get_id() == Candidate.CAID).first()

            # 这里要检查一下有无重复申请

            ca.APID.append(app1)
            db.session.add(app1)
            db.session.commit()
            print("done")
            return home()
    else:
        return render_template("error/LogInFirst.html")

@candidate_bp.route('/apply-delete/<id>', methods=['GET', 'POST'])
def delete_apply(id):
    if current_user.is_authenticated:
        app=Applying.query.filter(
            Applying.APID==id
        ).first()
        job1 = Jobs.query.filter(
            app.JID == Jobs.JID).first()
        ca = Candidate.query.filter(
            current_user.get_id() == Candidate.CAID).first()
        ca.APID.remove(app)
        job1.APID.remove(app)
        # 这里要检查一下有无重复申请
        db.session.delete(app)
        db.session.commit()
        print("done")
        return home()
    else:
        return render_template("error/LogInFirst.html")
