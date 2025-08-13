from models.grade import Grade
from models.student import Student
from models.user import db  # إضافة هذا السطر
from sqlalchemy import func

def add_grade(student_id, subject, grade_value, max_grade=100.0, exam_type=None, notes=None):
    """إضافة درجة لطالب"""
    grade = Grade(
        student_id=student_id,
        subject=subject,
        grade_value=grade_value,
        max_grade=max_grade,
        exam_type=exam_type,
        notes=notes
    )
    db.session.add(grade)
    db.session.commit()
    return grade

def get_student_grades(student_id):
    """الحصول على جميع درجات طالب"""
    return Grade.query.filter_by(student_id=student_id).order_by(Grade.date.desc()).all()

def get_class_grades(subject=None):
    """الحصول على درجات الصف"""
    query = Grade.query
    if subject:
        query = query.filter_by(subject=subject)
    return query.order_by(Grade.date.desc()).all()

def get_student_average(student_id):
    """حساب متوسط درجات طالب"""
    grades = get_student_grades(student_id)
    if not grades:
        return 0
    total_percentage = sum(grade.percentage for grade in grades)
    return round(total_percentage / len(grades), 2)

def get_subject_averages():
    """حساب متوسط الدرجات لكل مادة"""
    result = db.session.query(
        Grade.subject,
        func.avg(Grade.grade_value).label('avg_grade'),
        func.count(Grade.id).label('count')
    ).group_by(Grade.subject).all()
    
    averages = []
    for subject, avg_grade, count in result:
        averages.append({
            'subject': subject,
            'average': round(float(avg_grade), 2),
            'count': count
        })
    
    return averages