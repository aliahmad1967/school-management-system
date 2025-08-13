from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from models.student import Student
from models.attendance import Attendance
from utils.attendance_utils import mark_attendance, get_today_attendance, get_attendance_rate
from datetime import datetime

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/attendance')
@login_required
def index():
    """صفحة الحضور الرئيسية"""
    students = Student.query.all()
    today_attendance = get_today_attendance()
    
    # إنشاء خريطة للحضور الحالي بشكل آمن
    attendance_map = {}
    for att in today_attendance:
        attendance_map[att.student_id] = {
            'status': att.status,
            'notes': att.notes or ''
        }
    
    attendance_rate = get_attendance_rate()
    return render_template('attendance/mark.html', 
                         students=students, 
                         attendance_map=attendance_map,
                         attendance_rate=attendance_rate)

@attendance_bp.route('/attendance/mark', methods=['POST'])
@login_required
def mark():
    """تسجيل الحضور"""
    try:
        # معالجة كل حقل في النموذج
        for key, value in request.form.items():
            if key.startswith('student_'):
                # استخراج معرف الطالب من اسم الحقل
                student_id = int(key.split('_')[1])
                status = value
                # الحصول على الملاحظات المرتبطة بالطالب
                notes_key = f'notes_{student_id}'
                notes = request.form.get(notes_key, '')
                
                # تسجيل الحضور
                mark_attendance(student_id, status, notes if notes else None)
        
        flash('تم تسجيل الحضور بنجاح', 'success')
        return redirect(url_for('attendance.index'))
    
    except ValueError as e:
        flash('خطأ في البيانات المدخلة. تأكد من صحة المعرفات.', 'error')
        return redirect(url_for('attendance.index'))
    except Exception as e:
        flash(f'حدث خطأ أثناء تسجيل الحضور: {str(e)}', 'error')
        return redirect(url_for('attendance.index'))

@attendance_bp.route('/attendance/report')
@login_required
def report():
    """تقرير الحضور"""
    from utils.attendance_utils import get_weekly_attendance_report
    
    weekly_report = get_weekly_attendance_report()
    return render_template('attendance/report.html', weekly_report=weekly_report)

@attendance_bp.route('/attendance/api/today')
@login_required
def api_today():
    """API للحصول على حضور اليوم"""
    today_attendance = get_today_attendance()
    data = []
    for att in today_attendance:
        data.append({
            'student_id': att.student_id,
            'student_name': att.student.full_name,
            'status': att.status,
            'notes': att.notes
        })
    return jsonify(data)