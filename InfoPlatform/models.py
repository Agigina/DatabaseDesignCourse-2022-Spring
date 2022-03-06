from InfoPlatform import db

class Company(db.Model):
    CID = db.Column(db.Integer, primary_key=True,
                    nullable=False, autoincrement=True)
    CName = db.Column(db.String(1024), nullable=False)
    Corporate = db.Column(db.String(1024))
    Cphone = db.Column(db.String(11), unique=True, nullable=False)
    CInofrmation = db.Column(db.Text)
    PID = db.relationship('Project')
    CMID = db.relationship('CompanyManager')


class Project(db.Model):
    PID = db.Column(db.Integer, primary_key=True,
                    nullable=False, autoincrement=True)
    PName = db.Column(db.String(1024), nullable=False)
    PAddress = db.Column(db.Text, nullable=False)
    JID = db.relationship('Jobs')
    CID = db.Column(db.Integer, db.ForeignKey('company.CID'))
    PMID = db.relationship('ProjectManager')


class ProjectManager(db.Model):
    PMID = db.Column(db.Integer, primary_key=True,
                     nullable=False, autoincrement=True)
    authority = db.relationship('Authority', back_populates='project_manager', uselist=False)
    BID = db.Column(db.Integer, db.ForeignKey('basic_info.BID'))
    PID = db.Column(db.Integer, db.ForeignKey('project.PID'))
    basic_info=db.relationship('BasicInfo',back_populates='project_manager')


class CompanyManager(db.Model):
    CMID = db.Column(db.Integer, primary_key=True,
                     nullable=False, autoincrement=True)
    CID = db.Column(db.Integer, db.ForeignKey('company.CID'))
    authority = db.relationship('Authority', back_populates='company_manager', uselist=False)
    BID = db.Column(db.Integer, db.ForeignKey('basic_info.BID'))
    basic_info=db.relationship('BasicInfo',back_populates='company_manager')


class BasicInfo(db.Model):
    BID = db.Column(db.Integer, primary_key=True,
                    nullable=False, autoincrement=True)
    BName = db.Column(db.String(1024), nullable=False)
    BPortrait = db.Column(db.LargeBinary(length=4096))
    Bphone = db.Column(db.String(11), unique=True, nullable=False)
    IDCard = db.Column(db.String(18), nullable=False)
    UserType = db.Column(db.Integer, nullable=False)
    Password = db.Column(db.String(18), nullable=False)
    Bemail=db.Column(db.String(1024), nullable=False)
    BAddress=db.Column(db.Text)

    project_manager = db.relationship('ProjectManager', back_populates='basic_info', uselist=False)
    company_manager = db.relationship('CompanyManager', back_populates='basic_info', uselist=False)
    candidate = db.relationship('Candidate', back_populates='basic_info', uselist=False)


class Candidate(db.Model):
    CAID = db.Column(db.Integer, primary_key=True,
                     nullable=False, autoincrement=True)
    Ccategory = db.Column(db.String(1024), nullable=False)
    health = db.Column(db.LargeBinary(length=4096))
    Cexperience = db.Column(db.Integer)
    detailExperience = db.Column(db.Text)
    status = db.Column(db.Boolean, nullable=False)
    certification = db.Column(db.LargeBinary(length=4096))
    moreInfo = db.Column(db.Text)
    BID = db.Column(db.Integer, db.ForeignKey('basic_info.BID'))
    basic_info=db.relationship('BasicInfo',back_populates='candidate')

class Jobs(db.Model):
    JID = db.Column(db.Integer, primary_key=True,
                    nullable=False, autoincrement=True)
    Jname = db.Column(db.String(1024), nullable=False)
    salary = db.Column(db.Float(precision="10,2"))
    Jcategory = db.Column(db.String(1024))
    Jinformation = db.Column(db.Text, nullable=False)
    Jexperience = db.Column(db.Integer)
    PID = db.Column(db.Integer, db.ForeignKey('project.PID'))


class Authority(db.Model):
    AID = db.Column(db.Integer, primary_key=True,
                    nullable=False, autoincrement=True)
    editfile = db.Column(db.Boolean, nullable=False)
    checkbasicinfo = db.Column(db.Boolean, nullable=False)
    sendoffer = db.Column(db.Boolean, nullable=False)
    editoffer = db.Column(db.Boolean, nullable=False)
    PMID = db.Column(db.Integer, db.ForeignKey('project_manager.PMID'))
    project_manager=db.relationship('ProjectManager',back_populates='authority')
    CMID = db.Column(db.Integer, db.ForeignKey('company_manager.CMID'))
    company_manager=db.relationship('CompanyManager',back_populates='authority')
