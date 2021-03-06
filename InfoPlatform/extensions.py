from flask_bootstrap import Bootstrap
# from InfoPlatform.models import BasicInfo
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
ckeditor = CKEditor()
toolbar = DebugToolbarExtension()
migrate = Migrate()


@login_manager.user_loader
def load_user(user_id):
    from InfoPlatform.models import BasicInfo
    user = BasicInfo.query.get(int(user_id))
    return user


login_manager.login_view = 'anonymous'
# login_manager.login_message = 'Your custom message'
# login_manager.login_message_category = 'warning'
