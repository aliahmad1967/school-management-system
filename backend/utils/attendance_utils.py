from datetime import datetime, timedelta
from models.attendance import Attendance
from models.student import Student
from models.user import db

def get_today_attendance():
    """الحصول على حضور اليوم"""
    today = datetime.utcnow().date()
    return Attendance.query.filter_by(date=today).all()

def mark_attendance(student_id, status, notes=None):
    """تسجيل حضور طالب"""
    today = datetime.utcnow().date()
    
    # التحقق مما إذا كان الطالب قد سجل حضوره اليوم
    existing = Attendance.query.filter_by(
        student_id=student_id, 
        date=today
    ).first()
    
    if existing:
        # تحديث الحضور الموجود
        existing.status = status
        existing.notes = notes
    else:
        # إنشاء حضور جديد
        attendance = Attendance(
            student_id=student_id,
            date=today,
            status=status,
            notes=notes
        )
        db.session.add(attendance)
    
    db.session.commit()

def get_attendance_rate(date=None):
    """حساب نسبة الحضور"""
    if date is None:
        date = datetime.utcnow().date()
    
    total_students = Student.query.count()
    if total_students == 0:
        return 0
    
    present_count = Attendance.query.filter_by(
        date=date, 
        status='present'
    ).count()
    
    return round((present_count / total_students) * 100, 2)

def get_weekly_attendance_report():
    """تقرير الحضور الأسبوعي"""
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=7)
    
    report = []
    current_date = start_date
    
    while current_date <= end_date:
        present_count = Attendance.query.filter_by(
            date=current_date, 
            status='present'
        ).count()
        
        total_count = Student.query.count()
        rate = round((present_count / total_count) * 100, 2) if total_count > 0 else 0
        
        # الحصول على اسم اليوم بالعربية
        day_names = {
            'Saturday': 'السبت',
            'Sunday': 'الأحد',
            'Monday': 'الاثنين',
            'Tuesday': 'الثلاثاء',
            'Wednesday': 'الأربعاء',
            'Thursday': 'الخميس',
            'Friday': 'الجمعة'
        }
        
        day_name = day_names.get(current_date.strftime('%A'), current_date.strftime('%A'))
        
        report.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'day_name': day_name,
            'present': present_count,
            'total': total_count,
            'rate': rate
        })
        
        current_date += timedelta(days=1)
    
    return report