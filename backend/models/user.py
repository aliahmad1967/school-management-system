from flask_sqlalchemy import SQLAlchemy

# إنشاء كائن db خارجياً
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, teacher, student, parent
    full_name = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    # إضافة هذه الطرق لدعم Flask-Login
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)