# import os

# from werkzeug.middleware.proxy_fix import ProxyFix

# # =========================================================
# # MEMORY OPTIMIZATION FOR RENDER 512MB
# # =========================================================

# os.environ["OMP_NUM_THREADS"] = "1"
# os.environ["MKL_NUM_THREADS"] = "1"
# os.environ["YOLO_CONFIG_DIR"] = "/tmp/Ultralytics"


# import torch

# torch.set_num_threads(1)


# from flask import Flask, jsonify, send_from_directory
# from flask_cors import CORS
# from flask_migrate import Migrate
# from flask_jwt_extended import JWTManager


# from config.config import Config
# from database.db import db


# from src.routes.predict_routes import predict_bp
# from src.routes.health_routes import health_bp
# from src.routes.report_routes import report_bp
# from src.routes.auth_routes import auth_bp
# from src.routes.file_routes import file_bp
# from src.routes.dashboard_routes import dashboard_bp
# from src.routes.history_routes import history_bp
# from src.routes.chat_routes import chat_bp


# from src.logger import logging



# def create_app():

#     app = Flask(__name__)


#     # =====================================================
#     # RENDER PROXY FIX
#     # =====================================================

#     app.wsgi_app = ProxyFix(
#         app.wsgi_app,
#         x_for=1,
#         x_proto=1,
#         x_host=1,
#         x_prefix=1
#     )


#     # =====================================================
#     # CONFIG
#     # =====================================================

#     app.config.from_object(Config)


#     # =====================================================
#     # DATABASE
#     # =====================================================

#     db.init_app(app)


#     # =====================================================
#     # JWT
#     # =====================================================

#     app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY

#     jwt = JWTManager(app)



#     # =====================================================
#     # MIGRATION
#     # =====================================================

#     migrate = Migrate(
#         app,
#         db
#     )



#     # =====================================================
#     # CORS FIX
#     # =====================================================

#     CORS(
#         app,
#         origins=[
#             "https://pneumo-ai-app.onrender.com",
#             "http://localhost:5173"
#         ],
#         supports_credentials=True,
#         allow_headers=[
#             "Content-Type",
#             "Authorization",
#             "Accept"
#         ],
#         methods=[
#             "GET",
#             "POST",
#             "PUT",
#             "DELETE",
#             "OPTIONS"
#         ]
#     )



#     # =====================================================
#     # SERVE AI GENERATED FILES
#     # =====================================================


#     @app.route(
#         "/artifacts/<path:path>"
#     )
#     def serve_artifacts(path):

#         return send_from_directory(
#             "artifacts",
#             path
#         )



#     # =====================================================
#     # SERVE UPLOADED XRAYS
#     # =====================================================


#     @app.route(
#         "/uploads/<path:path>"
#     )
#     def serve_uploads(path):

#         return send_from_directory(
#             "static/uploads",
#             path
#         )



#     # =====================================================
#     # BLUEPRINTS
#     # =====================================================


#     app.register_blueprint(
#         health_bp
#     )

#     app.register_blueprint(
#         file_bp
#     )


#     app.register_blueprint(
#         predict_bp
#     )


#     app.register_blueprint(
#         report_bp
#     )


#     app.register_blueprint(
#         auth_bp
#     )


#     app.register_blueprint(
#         dashboard_bp
#     )


#     app.register_blueprint(
#         history_bp
#     )


#     app.register_blueprint(
#         chat_bp
#     )



#     # =====================================================
#     # ROOT
#     # =====================================================


#     @app.route("/")
#     def home():

#         return jsonify({

#             "status":"online",

#             "message":
#             "PneumoAI API is running"

#         }),200




#     logging.info(
#         "Flask App Initialized Successfully"
#     )



#     # create tables
#     with app.app_context():

#         db.create_all()



#     return app





# # =========================================================
# # GUNICORN ENTRY
# # =========================================================

# app = create_app()



# if __name__ == "__main__":

#     port = int(
#         os.environ.get(
#             "PORT",
#             5000
#         )
#     )


#     app.run(
#         host="0.0.0.0",
#         port=port,
#         debug=False
#     )





import os

from werkzeug.middleware.proxy_fix import ProxyFix

# =========================================================
# MEMORY OPTIMIZATION FOR RENDER 512MB
# =========================================================

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["YOLO_CONFIG_DIR"] = "/tmp/Ultralytics"


import torch

torch.set_num_threads(1)


from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


from config.config import Config
from database.db import db


from src.routes.predict_routes import predict_bp
from src.routes.health_routes import health_bp
from src.routes.report_routes import report_bp
from src.routes.auth_routes import auth_bp
from src.routes.file_routes import file_bp
from src.routes.dashboard_routes import dashboard_bp
from src.routes.history_routes import history_bp
from src.routes.chat_routes import chat_bp


from src.logger import logging


def create_app():

    app = Flask(__name__)

    # =====================================================
    # RENDER PROXY FIX
    # =====================================================

    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1,
        x_proto=1,
        x_host=1,
        x_prefix=1
    )

    # =====================================================
    # CONFIG
    # =====================================================

    app.config.from_object(Config)

    # Disable automatic trailing slash redirects (prevents 308 redirects stripping CORS headers)
    app.url_map.strict_slashes = False

    # =====================================================
    # DATABASE & JWT & MIGRATE
    # =====================================================

    db.init_app(app)
    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
    jwt = JWTManager(app)
    migrate = Migrate(app, db)

    # =====================================================
    # CORS FIX (Applied globally to all routes and blueprints)
    # =====================================================

    CORS(
        app,
        resources={r"/*": {"origins": "*"}},  # Applies CORS headers to every endpoint
        supports_credentials=True,
        allow_headers=["*"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    # Ensure preflight OPTIONS requests return HTTP 200 explicitly
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = app.make_default_options_response()
            return response

    # =====================================================
    # SERVE AI GENERATED FILES
    # =====================================================

    @app.route("/artifacts/<path:path>")
    def serve_artifacts(path):
        return send_from_directory("artifacts", path)

    # =====================================================
    # SERVE UPLOADED XRAYS
    # =====================================================

    @app.route("/uploads/<path:path>")
    def serve_uploads(path):
        return send_from_directory("static/uploads", path)

    # =====================================================
    # BLUEPRINTS
    # =====================================================

    app.register_blueprint(health_bp)
    app.register_blueprint(file_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(chat_bp)

    # =====================================================
    # ROOT
    # =====================================================

    @app.route("/")
    def home():
        return jsonify({
            "status": "online",
            "message": "PneumoAI API is running"
        }), 200

    logging.info("Flask App Initialized Successfully")

    with app.app_context():
        db.create_all()

    return app


# =========================================================
# GUNICORN ENTRY
# =========================================================

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)