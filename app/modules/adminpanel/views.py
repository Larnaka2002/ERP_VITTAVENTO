from flask import Blueprint, render_template

adminpanel_bp = Blueprint(
    name='adminpanel',
    import_name=__name__,
    template_folder='templates'
)

@adminpanel_bp.route('/', methods=['GET'])
def index():
    return render_template('adminpanel/index.html')