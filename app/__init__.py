from flask import Flask
from config import Config
from app.database import setup_db
from flask_session import Session

# Blueprint dashboard controller
from app.controllers.dashboard_controllers import dashboard_bp
# Blueprint Penerimaan controller
from app.controllers.penerimaan_controllers import penerimaan_bp
# Blueprint Penggunaan controller
from app.controllers.penggunaan_controllers import penggunaan_bp
# Blueprint pembelian controller
from app.controllers.pembelian_controllers import pembelian_bp
# Blueprint stok controller
from app.controllers.stok_controllers import stok_bp
# Blueprint riwayat
from app.controllers.riwayat_controllers import riwayat_bp
# Blueprint cek pakan ayam
from app.controllers.check_controllers import check_bp
# Blueprint user
from app.controllers.user_controllers import user_bp
# Blueprint auth
from app.controllers.auth_controllers import auth_bp



app = Flask(__name__, template_folder='templates', static_folder='assets', static_url_path='/assets')

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

app.config.from_object(Config)

# Setup database
setup_db(app)

app.register_blueprint(dashboard_bp)
app.register_blueprint(penerimaan_bp)
app.register_blueprint(penggunaan_bp)
app.register_blueprint(pembelian_bp)
app.register_blueprint(stok_bp)
app.register_blueprint(riwayat_bp)
app.register_blueprint(check_bp)
app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)
