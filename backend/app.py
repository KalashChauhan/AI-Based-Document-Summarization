import os
from flask import Flask,jsonify
from flask_cors import CORS
from config import Config
from models.database import init_db,close_db
from services.summarization_service import SummarizationService
from routes.summary_routes import summary_bp
from routes.document_routes import document_bp

def create_app(config_override=None):
    app=Flask(__name__); app.config.from_object(Config)
    if config_override: app.config.update(config_override)
    CORS(app,resources={r'/api/*':{'origins':'*'}}); init_db(app); 
    app.teardown_appcontext(close_db)
    app.extensions['summarizer']=SummarizationService(app.config['MODEL_NAME'])
    app.register_blueprint(summary_bp,url_prefix='/api'); 
    app.register_blueprint(document_bp,url_prefix='/api')
    @app.get('/api/health')
    def health(): 
        return jsonify(status='success',message='Backend is running')
    @app.errorhandler(413)
    def too_large(_): 
        return jsonify(success=False,error='File is too large. Maximum size is 10 MB.'),413
    return app

if __name__=='__main__':
    # Disable Flask's duplicate reloader process by default; opt in while developing.
    debug = os.getenv('FLASK_DEBUG', '').lower() in {'1', 'true', 'yes'}
    create_app().run(host='127.0.0.1', debug=debug, port=5000)
