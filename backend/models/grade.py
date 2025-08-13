from models.user import db  # هذا السطر صحيح
from datetime import datetime

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    grade_value = db.Column(db.Float, nullable=False)
    max_grade = db.Column(db.Float, default=100.0)
    exam_type = db.Column(db.String(50))  # اختبار, واجب, مشروع, إلخ
    date = db.Column(db.Date, default=datetime.utcnow)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # العلاقة مع الطالب
    student = db.relationship('Student', backref=db.backref('grades', lazy=True))
    
    def __repr__(self):
        return f'<Grade {self.student.full_name} - {self.subject} - {self.grade_value}>'
    
    @property
    def percentage(self):
        if self.max_grade:
            return round((self.grade_value / self.max_grade) * 100, 2)
        return 0