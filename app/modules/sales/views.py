from flask import Blueprint, render_template

sales_bp = Blueprint(
    name='sales',
    import_name=__name__,
    template_folder='templates'
)

@sales_bp.route('/', methods=['GET'])
def index():
    return render_template('sales/index.html')