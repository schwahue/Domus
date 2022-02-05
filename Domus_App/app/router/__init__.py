from flask import Blueprint, render_template

# Modules needed by Wilfred (maybe)
# from flask import Flask, render_template, redirect, url_for
# from flask_bootstrap import Bootstrap
# from flask_wtf import FlaskForm 
# from wtforms import StringField, PasswordField, BooleanField
# from wtforms.validators import InputRequired, Email, Length
# from flask_sqlalchemy  import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


router = Blueprint('router', __name__, template_folder='templates')

# This will help to render the navigation bar items [(href, id, caption)]
# Set active_page = id
pages = [('router.index', 'index', 'Index')]
admin_pages = [('router.admin_ticket', 'ticketing', 'Ticketing')]

@router.route('/')
def index():
    return render_template("index.html", navigation_bar = pages, active_page='index'), 200

@router.route('/admin')
def admin_index():
    return render_template("admin-index.html", navigation_bar = admin_pages), 200

ticketList = [('abc01', 'this is a ticket blah blah', 'resolved')]

@router.route('/admin/ticketing')
def admin_ticket():
    
    return render_template("admin-ticketing.html",  navigation_bar = admin_pages,
                                                    active_page='ticketing',
                                                    ticketList = ticketList ), 200


# CRUD
# List seller property
# Seller property page controls

# TODO: Use Cognito
@router.route('/user/login')
def simple_login():
    return login_page("property/login.html")


# TODO: Use RDS
@router.route('/user/property')
def admin_ticket():
    return render_template("admin-ticketing.html")

# 

