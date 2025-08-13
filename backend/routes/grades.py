from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from models.student import Student
from models.grade import Grade
from models.user import db
from utils.grade_utils import add_grade, get_student_grades, get_class_grades, get_student_average, get_subject_averages
from datetime import datetime

grades_bp = Blueprint('grades', __name__)

@grades_bp.route('/grades')
@login_required
def index():
    """صفحة الدرجات الرئيسية"""
    students = Student.query.all()
    # الحصول على المواد المختلفة
    subjects = db.session.query(Grade.subject).distinct().all()
    subject_list = [s[0] for s in subjects] if subjects else []
    
    return render_template('grades/index.html', students=students, subjects=subject_list)

@grades_bp.route('/grades/enter', methods=['GET', 'POST'])
@login_required
def enter_grades():
    """إدخال الدرجات"""
    if request.method == 'POST':
        try:
            subject = request.form['subject']
            exam_type = request.form.get('exam_type')
            max_grade = float(request.form.get('max_grade', 100))
            
            # إدخال درجات الطلاب
            for key, value in request.form.items():
                if key.startswith('grade_') and value:
                    student_id = int(key.split('_')[1])
                    grade_value = float(value)
                    
                    add_grade(
                        student_id=student_id,
                        subject=subject,
                        grade_value=grade_value,
                        max_grade=max_grade,
                        exam_type=exam_type
                    )
            
            flash('تم حفظ الدرجات بنجاح', 'success')
            return redirect(url_for('grades.index'))
            
        except ValueError as e:
            flash('خطأ في البيانات المدخلة. تأكد من إدخال أرقام صحيحة في الحقول الرقمية.', 'error')
            return redirect(url_for('grades.enter_grades'))
        except Exception as e:
            flash(f'حدث خطأ أثناء حفظ الدرجات: {str(e)}', 'error')
            return redirect(url_for('grades.enter_grades'))
    
    students = Student.query.all()
    return render_template('grades/enter.html', students=students)

@grades_bp.route('/grades/student/<int:student_id>')
@login_required
def student_grades(student_id):
    """عرض درجات طالب معين"""
    student = Student.query.get_or_404(student_id)
    grades = get_student_grades(student_id)
    average = get_student_average(student_id)
    
    return render_template('grades/student.html', student=student, grades=grades, average=average)

@grades_bp.route('/grades/report')
@login_required
def report():
    """تقرير الدرجات"""
    subject_averages = get_subject_averages()
    return render_template('grades/report.html', subject_averages=subject_averages)

@grades_bp.route('/grades/api/student/<int:student_id>')
@login_required
def api_student_grades(student_id):
    """API للحصول على درجات طالب"""
    grades = get_student_grades(student_id)
    data = []
    for grade in grades:
        data.append({
            'subject': grade.subject,
            'grade': grade.grade_value,
            'max_grade': grade.max_grade,
            'percentage': grade.percentage,
            'exam_type': grade.exam_type,
            'date': grade.date.strftime('%Y-%m-%d')
        })
    return jsonify(data)