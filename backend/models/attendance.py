from models.user import db
from datetime import datetime

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(10), nullable=False)  # present, absent, late
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # العلاقة مع الطالب
    student = db.relationship('Student', backref=db.backref('attendances', lazy=True))
    
    def __repr__(self):
        return f'<Attendance {self.student.full_name} - {self.date} - {self.status}>'