import qrcode
from io import BytesIO
import base64
import json

def generate_qr_code_base64(data):
    """توليد رمز QR وتحويله إلى base64"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # تحويل الصورة إلى base64
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

def generate_student_qr_data(student):
    """توليد بيانات QR للطالب"""
    student_data = {
        'id': student.id,
        'name': student.full_name,
        'student_id': student.student_id,
        'grade': student.grade
    }
    return json.dumps(student_data, ensure_ascii=False)