from models.user import db
import os

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.String(20), nullable=False)
    photo_path = db.Column(db.String(200))  # مسار الصورة
    parent_phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def __repr__(self):
        return f'<Student {self.full_name}>'
    
    @property
    def photo_url(self):
        if self.photo_path and os.path.exists(self.photo_path):
            return f"/uploads/{os.path.basename(self.photo_path)}"
        return "/static/images/default-avatar.png"