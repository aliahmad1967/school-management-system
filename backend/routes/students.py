from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required
from models.student import Student, db
import os
from werkzeug.utils import secure_filename

students_bp = Blueprint('students', __name__)

# السماح بأنواع معينة من الملفات
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_student_photo(file):
    """حفظ صورة الطالب"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # إنشاء مجلد uploads إذا لم يكن موجوداً
        upload_folder = os.path.join(current_app.root_path, 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        # حفظ الملف
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return f"uploads/{filename}"
    return None

@students_bp.route('/students')
@login_required
def list_students():
    students = Student.query.all()
    return render_template('students/list.html', students=students)

@students_bp.route('/students/add', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        try:
            # التحقق من وجود بيانات مطلوبة
            student_id = request.form.get('student_id', '').strip()
            full_name = request.form.get('full_name', '').strip()
            grade = request.form.get('grade', '').strip()
            
            if not student_id or not full_name or not grade:
                flash('يرجى ملء جميع الحقول المطلوبة', 'error')
                return render_template('students/add.html')
            
            # التحقق من عدم تكرار الرقم التعريفي
            existing_student = Student.query.filter_by(student_id=student_id).first()
            if existing_student:
                flash('الرقم التعريفي مستخدم بالفعل', 'error')
                return render_template('students/add.html')
            
            # حفظ الصورة إذا كانت موجودة
            photo_path = None
            if 'photo' in request.files:
                file = request.files['photo']
                if file and file.filename != '':
                    photo_path = save_student_photo(file)
            
            student = Student(
                student_id=student_id,
                full_name=full_name,
                grade=grade,
                parent_phone=request.form.get('parent_phone', ''),
                photo_path=photo_path
            )
            db.session.add(student)
            db.session.commit()
            flash('تم إضافة الطالب بنجاح', 'success')
            return redirect(url_for('students.list_students'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ أثناء إضافة الطالب: {str(e)}', 'error')
            return render_template('students/add.html')
    
    return render_template('students/add.html')

@students_bp.route('/students/<int:student_id>/card')
@login_required
def student_card(student_id):
    from utils.qr_generator import generate_qr_code_base64, generate_student_qr_data
    student = Student.query.get_or_404(student_id)
    # توليد رمز QR للطالب
    qr_data = generate_student_qr_data(student)
    qr_code = generate_qr_code_base64(qr_data)
    return render_template('students/card.html', student=student, qr_code=qr_code)

@students_bp.route('/students/<int:student_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    
    if request.method == 'POST':
        try:
            # التحقق من بيانات النموذج
            student_id_form = request.form.get('student_id', '').strip()
            full_name = request.form.get('full_name', '').strip()
            grade = request.form.get('grade', '').strip()
            
            if not student_id_form or not full_name or not grade:
                flash('يرجى ملء جميع الحقول المطلوبة', 'error')
                return render_template('students/edit.html', student=student)
            
            # التحقق من عدم تكرار الرقم التعريفي (إذا تغير)
            if student_id_form != student.student_id:
                existing_student = Student.query.filter_by(student_id=student_id_form).first()
                if existing_student:
                    flash('الرقم التعريفي مستخدم بالفعل', 'error')
                    return render_template('students/edit.html', student=student)
            
            # تحديث البيانات
            student.student_id = student_id_form
            student.full_name = full_name
            student.grade = grade
            student.parent_phone = request.form.get('parent_phone', '')
            
            # تحديث الصورة إذا تم رفع واحدة جديدة
            if 'photo' in request.files:
                file = request.files['photo']
                if file and file.filename != '':
                    photo_path = save_student_photo(file)
                    if photo_path:
                        student.photo_path = photo_path
            
            db.session.commit()
            flash('تم تحديث بيانات الطالب بنجاح', 'success')
            return redirect(url_for('students.list_students'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ أثناء تحديث الطالب: {str(e)}', 'error')
            return render_template('students/edit.html', student=student)
    
    return render_template('students/edit.html', student=student)

@students_bp.route('/students/<int:student_id>/delete', methods=['POST'])
@login_required
def delete_student(student_id):
    try:
        student = Student.query.get_or_404(student_id)
        # حذف ملف الصورة إذا وجد
        if student.photo_path and os.path.exists(os.path.join(current_app.root_path, student.photo_path)):
            os.remove(os.path.join(current_app.root_path, student.photo_path))
        
        db.session.delete(student)
        db.session.commit()
        flash('تم حذف الطالب بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ أثناء حذف الطالب: {str(e)}', 'error')
    
    return redirect(url_for('students.list_students'))