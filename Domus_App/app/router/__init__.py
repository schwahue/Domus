from flask import Blueprint, render_template

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

@router.route('/admin/ticketing')
def admin_ticket():
    return render_template("admin-ticketing.html", navigation_bar = admin_pages, active_page='ticketing'), 200
