from flask import render_template, flash, redirect, request, url_for, Blueprint
from flask_login import current_user
from InfoPlatform.utils import redirect_back
from InfoPlatform.forms import cmProfileForm,companyProfileForm,projectProfileForm
from InfoPlatform.models import BasicInfo, Candidate, Company, CompanyManager, Project, Jobs, Applying, ProjectManager
import datetime
from flask_uploads import UploadSet, IMAGES
import datetime
import os
from InfoPlatform.extensions import db

cm_bp = Blueprint('companymanager', __name__)
photos = UploadSet('photos', IMAGES)
color_map = [["#fee4cb", "#ff942e"], ["#e9e7fd", "#4f3ff0"], ["#dbf6fd", "#096c86"], ["#ffd3e2", "#df3670"],
             ["#c8f7dc", "#34c471"], ["#d5deff", "#4067f9"], ["#F6EEE0",
                                                              "#E4B7A0"], ["#FADCD9", "#F79489"], ["#ECE3F0", "#D3BBDD"]
             ]


@cm_bp.route('/home', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        projects = []
        print(current_user, current_user.get_id())
        cm = CompanyManager.query.filter(CompanyManager.id == current_user.get_id()).first()
        c = Company.query.filter(Company.CID == cm.CID).first()
        project = Project.query.filter(Project.CID == c.CID).all()
        
        basic_info = BasicInfo.query.filter(BasicInfo.id == current_user.get_id()).first()
        future = 0
        nowa = 0
        for i, item in enumerate(project):
            print(i,item.PName)
            d = item.Pbegin-datetime.datetime.now()
            if d.days > 0:
                future += 1
            else:
                nowa += 1
            if i >= len(color_map):
                    i -= len(color_map)
            progress = (datetime.datetime.now()-item.Pbegin).days / \
                (item.PEnd-item.Pbegin).days
            progress = 0 if progress < 0 else progress

            projects.append(
                {"begin": item.Pbegin, "thin": color_map[i][0], "thick": color_map[i][1], 
                 "end": item.PEnd,"progress_str": "%.2f%%" % (progress * 100), 
                 "proj_port": item.PPortrait.decode('ascii'), "Jddl": (item.PEnd-datetime.datetime.now()).days,"name": item.PName, "PID":item.PID})
        # 正在进行中和未开设
        print(len(projects))
        today = datetime.date.today()
        time_str = str(today.year)+"年"+str(today.month)+"月"+str(today.day)+"日"
        portrait = basic_info.BPortrait.decode('ascii')

        # return "a"
        return render_template("companymanager/base.html", time=time_str, future=future, img=portrait,
                               nowa=nowa, name=basic_info.BName, projects=projects, cmname=c.CName)
    else:
        return render_template("error/LogInFirst.html")


@cm_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if current_user.is_authenticated:
        form = cmProfileForm()
        if form.validate_on_submit():
            import base64
            # user = CompanyManager.query.filter(
            #     current_user.get_id() == CompanyManager.CAID).first()
            info = BasicInfo.query.filter(BasicInfo.id == current_user.get_id()).first()
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

            db.session.commit()
            return redirect(url_for('companymanager.home'))
        else:
            print(form.errors)
        return render_template("companymanager/profile.html", form=form)
    else:
        return render_template("error/LogInFirst.html")


@cm_bp.route('/project-profile/<id>', methods=['GET', 'POST'])
def project_profile(id):
    if current_user.is_authenticated:
        form = projectProfileForm()
        if form.validate_on_submit():
            project=Project.query.filter(Project.PID==id).first()

            cm = CompanyManager.query.filter(CompanyManager.id == current_user.get_id()).first()
            c = Company.query.filter(Company.CID == cm.CID).first()
            import base64
            print(form.data)
            portrait=form.portrait.data.filename
            form.portrait.data.save(portrait)
            portrait1 = open(portrait, 'rb')
            portrait1 = base64.b64encode(portrait1.read())
            os.remove(portrait)
            project.PName=form.nickname.data
            project.PAddress=form.Address.data
            project.PPortrait=portrait1
            project.Pbegin=form.begin.data
            project.PEnd=form.end.data
            # 搜索basicinfo。看看是projectmanager就绑定；如果是company就建立pm；如果是candidate就建立pm
            info=BasicInfo.query.filter(BasicInfo.id==form.pmid1.data).first()
            if info:
                pm=ProjectManager.query.filter(ProjectManager.id==info.id).first()
                if pm:
                    project.PMID.append(pm)
                else:
                    ca=Candidate.query.filter(Candidate.id==info.id).first()
                    if ca:
                        info.UserType=1
                        info.candidate=None
                        p_num=ProjectManager.query.count()
                        pm1=ProjectManager(PMID=p_num)
                        info.project_manager=pm1
                        project.PMID.append(pm1)
                        db.session.add(pm1)
                    else:
                        flash("公司管理员不可以作为项目管理员")
                        return redirect_back()
            else:
                print("no ")
                flash("不存在该用户")
                return redirect_back()
                # 登陆那种flash错误处理界面
            
            print("success")
            db.session.commit()
            return redirect(url_for('companymanager.home'))
        else:
            print(form.errors)
        return render_template("companymanager/project-profile.html", form=form)
    else:
        return render_template("error/LogInFirst.html")

@cm_bp.route('/add-project', methods=['GET', 'POST'])
def add_project():
    if current_user.is_authenticated:
        form = projectProfileForm()
        if form.validate_on_submit():
            cm = CompanyManager.query.filter(CompanyManager.id == current_user.get_id()).first()
            c = Company.query.filter(Company.CID == cm.CID).first()
            import base64
            print(form.data)
            portrait=form.portrait.data.filename
            form.portrait.data.save(portrait)
            portrait1 = open(portrait, 'rb')
            portrait1 = base64.b64encode(portrait1.read())
            os.remove(portrait)
            project1 = Project(PName=form.nickname.data, PAddress=form.Address.data,PPortrait=portrait1,
                           Pbegin=form.begin.data,
                           PEnd=form.end.data)

            # 搜索basicinfo。看看是projectmanager就绑定；如果是company就建立pm；如果是candidate就建立pm
            info=BasicInfo.query.filter(BasicInfo.id==form.pmid1.data).first()
            if info:
                pm=ProjectManager.query.filter(ProjectManager.id==info.id).first()
                if pm:
                    project1.PMID.append(pm)
                else:
                    ca=Candidate.query.filter(Candidate.id==info.id).first()
                    if ca:
                        info.UserType=1
                        info.candidate=None
                        p_num=ProjectManager.query.count()
                        pm1=ProjectManager(PMID=p_num)
                        info.project_manager=pm1
                        project1.PMID.append(pm1)
                        db.session.add(pm1)
                    else:
                        flash("公司管理员不可以作为项目管理员")
                        return redirect_back()
            else:
                print("no ")
                flash("不存在该用户")
                return redirect_back()
                # 登陆那种flash错误处理界面
            
            print("success")
            c.PID.append(project1)
            db.session.add(project1)
            db.session.commit()
            return redirect(url_for('companymanager.home'))
        else:
            print(form.errors)
        return render_template("companymanager/project-profile.html", form=form)
    else:
        return render_template("error/LogInFirst.html")

@cm_bp.route('/delete-project/<id>', methods=['GET', 'POST'])
def delete(id):
    if current_user.is_authenticated:
        cm = CompanyManager.query.filter(CompanyManager.id == current_user.get_id()).first()
        c = Company.query.filter(Company.CID == cm.CID).first()
        project=Project.query.filter(Project.PID==id).first()
        pm=ProjectManager.query.filter(ProjectManager.PID==Project.PMID).all()
        for item in pm:
            # 恢复candidate身份
            somthin=None
        c.PID.remove(project)
        db.session.commit()
        return home()
    else:
        return render_template("error/LogInFirst.html")

@cm_bp.route('/company-profile', methods=['GET', 'POST'])
def company_profile():
    if current_user.is_authenticated:
        form = companyProfileForm()
        if form.validate_on_submit():
            import base64
            cm = CompanyManager.query.filter(CompanyManager.id == current_user.get_id()).first()
            c = Company.query.filter(Company.CID == cm.CID).first()
            c.CName=form.nickname.data
            if form.corporate.data:
                c.Corporate=form.corporate.data
            c.Cphone=form.phone.data
            c.CInformation
                       
            portrait=form.portrait.data.filename
            form.portrait.data.save(portrait)
            portrait1 = open(portrait, 'rb')
            portrait1 = base64.b64encode(portrait1.read())
            os.remove(portrait)
            c.CPortrait = portrait1

            db.session.commit()
            return redirect(url_for('companymanager.home'))
        else:
            print(form.errors)
        return render_template("companymanager/company-profile.html", form=form)
    else:
        return render_template("error/LogInFirst.html")

