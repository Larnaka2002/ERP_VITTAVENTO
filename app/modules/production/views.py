from flask import Blueprint, render_template

production_bp = Blueprint(
    name='production',
    import_name=__name__,
    template_folder='templates'
)

@production_bp.route('/', methods=['GET'])
def index():
    return render_template('production/index.html')