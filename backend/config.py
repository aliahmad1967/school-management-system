import os

# الحصول على المسار الكامل لمجلد database
database_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database')
database_path = os.path.join(database_dir, 'school.db')

# التأكد من وجود المجلد
os.makedirs(database_dir, exist_ok=True)

class Config:
    SECRET_KEY = 'school-management-secret-key-2024'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{database_path}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False