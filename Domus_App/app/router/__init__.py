from flask import Blueprint, render_template

router = Blueprint('router', __name__, template_folder='templates')

@router.route('/')
def index():
    return render_template("listings.html"), 200

@router.route('/listings')
def listings():
    return render_template("listings.html"), 200