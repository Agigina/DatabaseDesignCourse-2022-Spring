from flask import render_template, flash, redirect, request, url_for, Blueprint
from flask_login import current_user

from InfoPlatform.forms import cmProfileForm
from InfoPlatform.models import Candidate, BasicInfo, Company, CompanyManager, Project, Jobs, Applying
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
        # BID = session['info_id']
        # print(BID)s
        print(current_user, current_user.get_id())
        cm = CompanyManager.query.filter(CompanyManager.id == current_user.get_id()).first()
        c = Company.query.filter(Company.CID == cm.CID).first()
        project = Project.query.filter(Project.CID == c.CID).all()
        basic_info = BasicInfo.query.filter(BasicInfo.id == current_user.get_id()).first()
        future = 0
        nowa = 0
        for i, item in enumerate(project):
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
    return "a"

@cm_bp.route('/add-project', methods=['GET', 'POST'])
def add_project():
    return "a"