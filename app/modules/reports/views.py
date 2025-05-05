from flask import Blueprint, render_template

reports_bp = Blueprint(
    name='reports',
    import_name=__name__,
    template_folder='templates'
)

@reports_bp.route('/', methods=['GET'])
def index():
    return render_template('reports/index.html')