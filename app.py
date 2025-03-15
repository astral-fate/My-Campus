from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
import os

# Initialize extensions first, without the app
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # Initialize Flask app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'  # Replace with a secure secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campus.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Assuming routes are organized in blueprints
    
    with app.app_context():
        db.create_all()
    
    # Register blueprints (this is where you'd import routes)
    from auth.routes import auth_bp
    from main.routes import main_bp
    from admin.routes import admin_bp
    from student.routes import student_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(student_bp, url_prefix='/student')
    
    return app

# Create the app instance
app = create_app()

# Export both app and db for other modules to use
if __name__ == '__main__':
    app.run(debug=True)