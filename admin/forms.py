from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError, Optional

# --- FORM LAMA: RejectForm (Pastikan ini tetap ada) ---
class RejectForm(FlaskForm):
    alasan = TextAreaField('Alasan Penolakan', validators=[
        DataRequired(message="Alasan penolakan wajib diisi."), 
        Length(min=10, message="Alasan harus lebih dari 10 karakter.")
    ])
    submit = SubmitField('Tolak Permintaan')

# --- FORM BARU: LecturerForm ---
class LecturerForm(FlaskForm):
    nama = StringField('Nama Lengkap Dosen', validators=[
        DataRequired(), 
        Length(min=3, max=150)
    ])
    nidn = StringField('NIDN', validators=[
        DataRequired(), 
        Length(min=5, max=20)
    ])
    fakultas = SelectField('Fakultas/Departemen', choices=[
        ('Fakultas TI', 'Fakultas Teknik Informatika'),
        ('Fakultas Ekonomi', 'Fakultas Ekonomi & Bisnis'),
        ('Fakultas Hukum', 'Fakultas Hukum'),
        ('Umum', 'Mata Kuliah Umum (MKU)')
    ], validators=[DataRequired()])
    submit = SubmitField('Simpan Dosen')

    # Validasi unik NIDN saat menambah dosen baru
    def validate_nidn(self, nidn):
        from models import Lecturer
        # Cek jika form sedang diedit (ada Lecturer ID di form)
        if hasattr(self, 'lecturer_id') and self.lecturer_id.data:
            lecturer = Lecturer.query.filter(Lecturer.nidn == nidn.data, Lecturer.id != self.lecturer_id.data).first()
        else:
            lecturer = Lecturer.query.filter_by(nidn=nidn.data).first()
            
        if lecturer:
            raise ValidationError('NIDN ini sudah terdaftar. Gunakan NIDN lain.')