from flask import Blueprint, render_template
from flask_login import login_required
from models.student import Student
from models.attendance import Attendance
from models.grade import Grade
from models.user import db
from datetime import datetime, date
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def index():
    # إحصائيات حقيقية من قاعدة البيانات
    total_students = Student.query.count()
    total_teachers = 0  # سيتم تحديثها لاحقاً عندما نضيف نموذج المعلم
    
    # حساب نسبة الحضور اليومي
    today = date.today()
    total_present_today = Attendance.query.filter_by(
        date=today, 
        status='present'
    ).count()
    
    attendance_rate = 0
    if total_students > 0:
        attendance_rate = round((total_present_today / total_students) * 100, 2)
    
    # حساب متوسط الدرجات
    avg_grade_result = db.session.query(func.avg(Grade.grade_value)).first()
    avg_grade = round(float(avg_grade_result[0]), 2) if avg_grade_result[0] else 0
    
    # تحديد مستوى الأداء
    if avg_grade >= 90:
        performance = "ممتاز"
    elif avg_grade >= 80:
        performance = "جيد جداً"
    elif avg_grade >= 70:
        performance = "جيد"
    elif avg_grade >= 60:
        performance = "مقبول"
    else:
        performance = "ضعيف"
    
    # بيانات تجريبية للأنشطة الأخيرة
    recent_activities = [
        {
            'description': 'تم تسجيل حضور الطالب أحمد محمد',
            'time': 'قبل 10 دقائق'
        },
        {
            'description': 'تم إدخال درجات مادة الرياضيات',
            'time': 'قبل ساعة'
        },
        {
            'description': 'تم دفع رسوم دراسية للطالب فاطمة علي',
            'time': 'قبل 3 ساعات'
        }
    ]
    
    stats = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'attendance_rate': f"{attendance_rate}%",
        'performance': performance
    }
    
    return render_template('dashboard.html', 
                         stats=stats, 
                         recent_activities=recent_activities,
                         avg_grade=avg_grade)