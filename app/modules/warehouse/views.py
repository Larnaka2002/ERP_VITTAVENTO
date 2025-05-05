from flask import Blueprint, render_template

warehouse_bp = Blueprint(
    name='warehouse',
    import_name=__name__,
    template_folder='templates'
)

@warehouse_bp.route('/', methods=['GET'])
def index():
    return render_template('warehouse/index.html')