from flask import render_template, flash, redirect, request, url_for, Blueprint
from flask_login import current_user
from InfoPlatform.utils import redirect_back
from InfoPlatform.forms import pmProfileForm,JobForm
from InfoPlatform.models import BasicInfo, Candidate, Company, CompanyManager, Project, Jobs, Applying, ProjectManager
import datetime
from flask_uploads import UploadSet, IMAGES
import datetime
from InfoPlatform.extensions import db

pm_bp = Blueprint('projectmanager', __name__)
photos = UploadSet('photos', IMAGES)
color_map = [["#fee4cb", "#ff942e"], ["#e9e7fd", "#4f3ff0"], ["#dbf6fd", "#096c86"], ["#ffd3e2", "#df3670"],
             ["#c8f7dc", "#34c471"], ["#d5deff", "#4067f9"], ["#F6EEE0",
                                                              "#E4B7A0"], ["#FADCD9", "#F79489"], ["#ECE3F0", "#D3BBDD"]
             ]

@pm_bp.route('/home', methods=['GET', 'POST'])
def home():
    # 左边是工作，右边是待处理的apply，删除左栏和搜索栏；添加+的按钮；工作对标项目；apply另写
    if current_user.is_authenticated:
        applyies = []
        jobs=[]
        print(current_user, current_user.get_id())
        pm = ProjectManager.query.filter(ProjectManager.id == current_user.get_id()).first()
        p = Project.query.filter(Project.PID == pm.PID).first()
        job = Jobs.query.filter(Jobs.PID == p.PID).all()
        
        
        info = BasicInfo.query.filter(BasicInfo.id == current_user.get_id()).first()
        future = 0
        nowa = 0
        for i, item in enumerate(job):
            
            d = item.JBegin-datetime.datetime.now()
            if d.days > 0:
                future += 1
            else:
                nowa += 1
            
            if i >= len(color_map):
                    i -= len(color_map)
            progress = (datetime.datetime.now()-item.JBegin).days / \
                (item.JFinal-item.JBegin).days
            progress = 0 if progress < 0 else progress
            jobs.append(
                    {"JBegin": str(item.JBegin.date()), "JFinal": str(item.JFinal.date()), "Jname": item.Jname,
                     "Jinformation": item.Jinformation, "Jddl": (item.Jddl-datetime.datetime.now()).days,
                     "thin": color_map[i][0], "thick": color_map[i][1], 
                     "progress_str": "%.2f%%" % (progress * 100),"JID":item.JID})
            apply=Applying.query.filter(Applying.JID==item.JID).all()
            for ap in apply:
                ca=Candidate.query.filter(Candidate.CAID==ap.CAID).first()
                cainfo=BasicInfo.query.filter(ca.id==BasicInfo.id).first()
                apply_time = "申请时间："+str(ap.applytime.date())
                applyies.append({"applytime": apply_time, "proj_name": p.PName,"cname":cainfo.BName,"phone":cainfo.Bphone,
                                    "job_name": item.Jname, "Info": "类型："+str(item.Jcategory)+"，信息："+str(item.Jinformation),
                                    "PPortrait": p.PPortrait.decode('ascii'),"APID":ap.APID})
        # 正在进行中和未开设
        today = datetime.date.today()
        time_str = str(today.year)+"年"+str(today.month)+"月"+str(today.day)+"日"
        portrait = info.BPortrait.decode('ascii')

        return render_template("projectmanager/base.html",projectname=p.PName,name=info.BName,
                               time=time_str,nowa=nowa,future=future,img=portrait,
                               available_job=jobs,applying_list=applyies)
    # projectname

    # name
    else:
        return render_template("error/LogInFirst.html")

@pm_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if current_user.is_authenticated:
        form = pmProfileForm()
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


@pm_bp.route('/job-profile/<id>', methods=['GET', 'POST'])
def job_profile(id):
    return "A"

@pm_bp.route('/delete-job/<id>', methods=['GET', 'POST'])
def delete(id):
    return "A"

@pm_bp.route('/offer/<id>', methods=['GET', 'POST'])
def offer(id):
    return "A"

@pm_bp.route('/refuse/<id>', methods=['GET', 'POST'])
def refuse(id):
    return "A"

@pm_bp.route('/add-project', methods=['GET', 'POST'])
def add():
    return "A"