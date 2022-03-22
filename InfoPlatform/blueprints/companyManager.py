from asyncio.windows_events import NULL
from flask import render_template, flash, redirect, request, url_for, Blueprint
from flask_login import current_user

from InfoPlatform.forms import ProfileForm
from InfoPlatform.models import Candidate, BasicInfo, Project, Jobs, Applying
import datetime
from flask_uploads import UploadSet, IMAGES

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
        projects=[]
        # 正在进行中和未开设
        return render_template("companymanager/base.html", time=time_str, recruiting=recruiting,
                               img=portrait, name=basic_info.BName, applying_list=applying_list,
                               available_job=available_job, waiting_num=waiting_num, offer_num=offer_num)
    else:
        return render_template("error/LogInFirst.html")
