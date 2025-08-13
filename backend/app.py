from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from models.user import db, User
import os

# الحصول على المسار الكامل لمجلد القوالب
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config.from_object(Config)

# إضافة مجلد uploads كمسار ثابت
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

# إعداد قاعدة البيانات
db.init_app(app)

# إعداد نظام تسجيل الدخول
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# تسجيل المسارات
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.students import students_bp
from routes.attendance import attendance_bp
from routes.grades import grades_bp

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(students_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(grades_bp)

# إنشاء الجداول
with app.app_context():
    db.create_all()
    
    # إنشاء مستخدم تجريبي
    if not User.query.first():
        admin = User(
            username='admin',
            password='admin123',  # في الإنتاج استخدم تشفير كلمة المرور
            role='admin',
            full_name='مدير النظام'
        )
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)