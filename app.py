from flask import Flask, render_template, redirect, url_for, session
from flask_login import LoginManager, current_user
import os
from config import Config
from utils.data_handler import initialize_data

app = Flask(__name__)
app.config.from_object(Config)

# Explicitly set secret key for sessions
app.secret_key = app.config['SECRET_KEY']

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Initialize data files
initialize_data()

# Import routes
from routes import auth, dashboard, trading, contracts

# Register blueprints
app.register_blueprint(auth.bp)
app.register_blueprint(dashboard.bp)
app.register_blueprint(trading.bp)
app.register_blueprint(contracts.bp)

@login_manager.user_loader
def load_user(user_id):
    from models.user import User
    return User.get_by_id(user_id)

@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.user_type == 'buyer':
            return redirect(url_for('dashboard.buyer_dashboard'))
        else:
            return redirect(url_for('dashboard.seller_dashboard'))
    return redirect(url_for('auth.login'))  # FIXED: Removed extra quote

if __name__ == '__main__':
    # Port 7860 is required for Hugging Face Spaces
    port = int(os.environ.get('PORT', 7860))
    app.run(debug=False, host='0.0.0.0', port=port)
