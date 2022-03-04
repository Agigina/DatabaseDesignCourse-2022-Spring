import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler

import click
from flask import Flask, render_template, request
from flask_login import current_user
from flask_sqlalchemy import get_debug_queries
from flask_wtf.csrf import CSRFError

from InfoPlatform.blueprints.candidate import candidate_bp

from InfoPlatform.models import Company,Project,ProjectManager,CompanyManager,BasicInfo,Candidate,Jobs,Authority
from InfoPlatform.settings import config

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
