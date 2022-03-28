import os

import click
from flask import Flask, render_template, request
from flask_login import current_user
from flask_wtf.csrf import CSRFError
from InfoPlatform.extensions import bootstrap, db, login_manager, csrf, ckeditor, toolbar, migrate
import datetime

from InfoPlatform.blueprints.candidate import candidate_bp
from InfoPlatform.blueprints.anonymous import anonymous_bp
from InfoPlatform.blueprints.companyManager import cm_bp
from InfoPlatform.blueprints.projectManager import pm_bp

from InfoPlatform.models import Company, Project, ProjectManager, CompanyManager, BasicInfo, Candidate, Jobs, Authority, Applying
from InfoPlatform.settings import config

from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('InfoPlatform')
    app.config.from_object(config[config_name])
    photos = UploadSet('photos', IMAGES)
    configure_uploads(app, photos)
    patch_request_class(app)    # register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    #  # register_errors(app)
    # register_shell_context(app)
    # register_template_context(app)
    # register_request_handlers(app)
    return app


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    ckeditor.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    app.register_blueprint(anonymous_bp)
    app.register_blueprint(candidate_bp, url_prefix='/candidate')
    app.register_blueprint(cm_bp, url_prefix='/companymanager')
    app.register_blueprint(pm_bp, url_prefix='/projectmanager')


# def register_shell_context(app):
#     @app.shell_context_processor
#     def make_shell_context():
#         return dict(db=db, Admin=Admin, Post=Post, Category=Category, Comment=Comment)


def register_commands(app):
    @app.cli.command()
    def forge():
        db.drop_all()
        db.create_all()
        click.echo('Done.')

    @app.cli.command()
    def fake():
        import base64

        portrait1 = open("InfoPlatform/static/image/portrait1.jpg", 'rb')
        portrait1 = base64.b64encode(portrait1.read())
        portrait2 = open("InfoPlatform/static/image/portrait2.jpg", 'rb')
        portrait2 = base64.b64encode(portrait2.read())
        portrait3 = open("InfoPlatform/static/image/portrait3.jpg", 'rb')
        portrait3 = base64.b64encode(portrait3.read())
        portrait4 = open("InfoPlatform/static/image/portrait4.jpg", 'rb')
        portrait4 = base64.b64encode(portrait4.read())

        bi1 = BasicInfo(BName="赵艺博", Bphone="18335320958", BPortrait=portrait1,
                        IDCard="140302200108031228", UserType=1, Password="12", Bemail="zybzyb_email@163.com")
        bi2 = BasicInfo(BName="邹玉洁", Bphone="15235327868", BPortrait=portrait2,
                        IDCard="140302200108031227", UserType=2, Password="123", Bemail="139@qq.com")
        bi3 = BasicInfo(BName="谢佳依", Bphone="15235327867", BPortrait=portrait3,
                        IDCard="140302200108031226", UserType=0, Password="1234", Bemail="163@gmail.com")
        bi4 = BasicInfo(BName="刘珺益", Bphone="15235327866", BPortrait=portrait4,
                        IDCard="140302200108031225", UserType=1, Password="12345", Bemail="123@126.com")

        pportrait1 = open("InfoPlatform/static/image/pportrait1.jpg", 'rb')
        pportrait1 = base64.b64encode(pportrait1.read())
        pportrait2 = open("InfoPlatform/static/image/pportrait2.jpg", 'rb')
        pportrait2 = base64.b64encode(pportrait2.read())
        cportrait1 = open("InfoPlatform/static/image/cportrait1.jpg", 'rb')
        cportrait1 = base64.b64encode(cportrait1.read())

        project1 = Project(PName="上海市十号线修筑工程", PAddress="上海市杨浦区国帆路", PPortrait=pportrait1,
                           Pbegin=datetime.datetime.strptime(
                               "2022-1-9 00:01:01", '%Y-%m-%d %H:%M:%S'),
                           PEnd=datetime.datetime.strptime("2022-11-10 00:01:01", '%Y-%m-%d %H:%M:%S'))
        project2 = Project(PName="苏州体育馆承建", PAddress="苏州市", PPortrait=pportrait2,
                           Pbegin=datetime.datetime.strptime(
                               "2022-3-9 00:01:01", '%Y-%m-%d %H:%M:%S'),
                           PEnd=datetime.datetime.strptime("2022-11-10 00:01:01", '%Y-%m-%d %H:%M:%S'))
        com = Company(CName="上海七维建筑工程有限公司", Corporate="某法人", CPortrait=cportrait1,
                      Cphone="15266332255", CInformation="嘟嘟嘟噜噜噜玛卡巴卡玛卡巴卡")

        pm = ProjectManager(PMID=0)
        cm = CompanyManager(CMID=0)
        job1 = Jobs(Jname="LNG接收站施工工程师（土建）", salary=13000, Jcategory="全职",
                    Jinformation="全职，不允许远程", Jexperience=0, Jddl=datetime.datetime.strptime("2022-5-1 00:01:01", '%Y-%m-%d %H:%M:%S'),
                    JBegin=datetime.datetime.strptime("2022-3-4 00:01:01", '%Y-%m-%d %H:%M:%S'), JFinal=datetime.datetime.strptime("2022-6-18 00:01:01", '%Y-%m-%d %H:%M:%S'))
        job2 = Jobs(Jname="土建施工员G00961", salary=16000, Jcategory="全职",
                    Jinformation="全职，不允许远程", Jexperience=0, Jddl=datetime.datetime.strptime("2022-6-1 00:01:01", '%Y-%m-%d %H:%M:%S'),
                    JBegin=datetime.datetime.strptime("2022-3-9 00:01:01", '%Y-%m-%d %H:%M:%S'), JFinal=datetime.datetime.strptime("2022-8-18 00:01:01", '%Y-%m-%d %H:%M:%S'))
        job3 = Jobs(Jname="土建施工图设计师", salary=21000, Jcategory="全职",
                    Jinformation="全职，不允许远程", Jexperience=0, Jddl=datetime.datetime.strptime("2022-4-1 00:01:01", '%Y-%m-%d %H:%M:%S'),
                    JBegin=datetime.datetime.strptime("2022-1-9 00:01:01", '%Y-%m-%d %H:%M:%S'), JFinal=datetime.datetime.strptime("2022-4-21 00:01:01", '%Y-%m-%d %H:%M:%S'))
        job4 = Jobs(Jname="现场土建负责人", salary=7000, Jcategory="全职",
                    Jinformation="全职，不允许远程", Jexperience=0, Jddl=datetime.datetime.strptime("2022-9-1 00:01:01", '%Y-%m-%d %H:%M:%S'),
                    JBegin=datetime.datetime.strptime("2022-5-1 00:01:01", '%Y-%m-%d %H:%M:%S'), JFinal=datetime.datetime.strptime("2022-9-28 00:01:01", '%Y-%m-%d %H:%M:%S'))
        job5 = Jobs(Jname="土建施工员", salary=8000, Jcategory="全职", Jinformation="全职，不允许远程", Jddl=datetime.datetime.strptime("2022-9-1 00:01:01", '%Y-%m-%d %H:%M:%S'),
                    Jexperience=0, JBegin=datetime.datetime.strptime("2022-3-14 00:01:01", '%Y-%m-%d %H:%M:%S'), JFinal=datetime.datetime.strptime("2022-9-14 00:01:01", '%Y-%m-%d %H:%M:%S'))
        job6 = Jobs(Jname="园林土建施工员", salary=16000, Jcategory="全职", Jinformation="全职，不允许远程", Jddl=datetime.datetime.strptime("2022-10-1 00:01:01", '%Y-%m-%d %H:%M:%S'),
                    Jexperience=0, JBegin=datetime.datetime.strptime("2022-3-19 00:01:01", '%Y-%m-%d %H:%M:%S'), JFinal=datetime.datetime.strptime("2022-10-18 00:01:01", '%Y-%m-%d %H:%M:%S'))
        job7 = Jobs(Jname="园林土建主施工员", salary=13000, Jcategory="全职", Jddl=datetime.datetime.strptime("2022-11-1 00:01:01", '%Y-%m-%d %H:%M:%S'),
                    Jinformation="全职，不允许远程", Jexperience=0, JBegin=datetime.datetime.strptime("2022-4-9 00:01:01", '%Y-%m-%d %H:%M:%S'), JFinal=datetime.datetime.strptime("2022-11-9 00:01:01", '%Y-%m-%d %H:%M:%S'))
        job8 = Jobs(Jname="施工员（土建）", salary=6000, Jcategory="全职", Jinformation="全职，不允许远程", Jddl=datetime.datetime.strptime("2022-11-1 00:01:01", '%Y-%m-%d %H:%M:%S'),
                    Jexperience=0, JBegin=datetime.datetime.strptime("2022-4-19 00:01:01", '%Y-%m-%d %H:%M:%S'), JFinal=datetime.datetime.strptime("2022-11-9 00:01:01", '%Y-%m-%d %H:%M:%S'))
        job9 = Jobs(Jname="土建施工员", salary=6000, Jcategory="全职", Jinformation="全职，不允许远程", Jddl=datetime.datetime.strptime("2022-5-1 00:01:01", '%Y-%m-%d %H:%M:%S'),
                    Jexperience=0, JBegin=datetime.datetime.strptime("2022-3-4 00:01:01", '%Y-%m-%d %H:%M:%S'), JFinal=datetime.datetime.strptime("2022-6-18 00:01:01", '%Y-%m-%d %H:%M:%S'))
        job9 = Jobs(Jname="土建施工员", salary=6000, Jcategory="全职", Jinformation="全职，不允许远程", Jddl=datetime.datetime.strptime("2022-5-1 00:01:01", '%Y-%m-%d %H:%M:%S'),
                    Jexperience=0, JBegin=datetime.datetime.strptime("2022-3-4 00:01:01", '%Y-%m-%d %H:%M:%S'), JFinal=datetime.datetime.strptime("2022-6-18 00:01:01", '%Y-%m-%d %H:%M:%S'))

        health = open("InfoPlatform/static/image/health.jpg", 'rb')
        health = base64.b64encode(health.read())
        certificate = open("InfoPlatform/static/image/certificate.jpg", 'rb')
        certificate = base64.b64encode(certificate.read())
        ca = Candidate(Ccategory="焊工", health=health, Cexperience=2, detailExperience="曾在多家企业实习。",
                       status=False, certification=certificate, moreInfo="现居住上海，希望本地工作。")

        bi1.candidate = ca
        bi2.project_manager = pm
        bi3.company_manager = cm

        com.CMID.append(cm)
        project1.PMID.append(pm)

        project1.JID.append(job1)
        project1.JID.append(job3)
        project1.JID.append(job5)
        project1.JID.append(job7)
        project1.JID.append(job9)
        project2.JID.append(job2)
        project2.JID.append(job4)
        project2.JID.append(job6)
        project2.JID.append(job8)

        com.PID.append(project1)
        com.PID.append(project2)

        app1 = Applying(applytime=datetime.datetime.strptime(
            "2022-2-15 00:01:01", '%Y-%m-%d %H:%M:%S'), status=int(0))
        app2 = Applying(applytime=datetime.datetime.strptime(
            "2022-2-12 00:01:01", '%Y-%m-%d %H:%M:%S'), status=int(1))
        app3 = Applying(applytime=datetime.datetime.strptime(
            "2022-2-16 00:01:01", '%Y-%m-%d %H:%M:%S'), status=int(2))

        job1.APID.append(app1)
        job2.APID.append(app2)
        job3.APID.append(app3)

        ca.APID.append(app1)
        ca.APID.append(app2)
        ca.APID.append(app3)

        db.session.add(bi1)
        db.session.add(bi2)
        db.session.add(bi3)
        db.session.add(bi4)

        db.session.add(project1)
        db.session.add(project2)
        db.session.add(com)

        db.session.add(pm)
        db.session.add(cm)

        db.session.add(job1)
        db.session.add(job2)
        db.session.add(job3)
        db.session.add(job4)
        db.session.add(job5)
        db.session.add(job6)
        db.session.add(job7)
        db.session.add(job8)
        db.session.add(job9)

        db.session.add(ca)
        db.session.add(app1)
        db.session.add(app2)
        db.session.add(app3)

        db.session.commit()

    @app.cli.command()
    def check():
        print(Candidate.query.all())
        print(BasicInfo.query.all())
        print(CompanyManager.query.all())
        print(ProjectManager.query.all())
        print(Company.query.all())

        print(Project.query.all())

        # for item in Jobs.query.filter(Jobs.salary>100.00).all():
        #     print(item.Jname)
        # print(Jobs.query.filter(Jobs.salary>100.00).first().Jname)
        click.echo('建议直接打开db看.')
