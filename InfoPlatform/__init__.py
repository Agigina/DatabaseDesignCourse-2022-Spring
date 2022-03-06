import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler

import click
from flask import Flask, render_template, request
from flask_login import current_user
from flask_sqlalchemy import get_debug_queries
from flask_wtf.csrf import CSRFError
from InfoPlatform.extensions import bootstrap, db, login_manager, csrf, ckeditor, toolbar, migrate

from InfoPlatform.blueprints.candidate import candidate_bp
from InfoPlatform.blueprints.anonymous import anonymous_bp

from InfoPlatform.models import Company,Project,ProjectManager,CompanyManager,BasicInfo,Candidate,Jobs,Authority
from InfoPlatform.settings import config


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('InfoPlatform')
    app.config.from_object(config[config_name])

    # register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    # register_errors(app)
    register_shell_context(app)
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
    # app.register_blueprint(admin_bp, url_prefix='/admin')
    # app.register_blueprint(auth_bp, url_prefix='/auth')

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Admin=Admin, Post=Post, Category=Category, Comment=Comment)


def register_commands(app):
    @app.cli.command()
    def forge():
        db.drop_all()
        db.create_all()
        click.echo('Done.')