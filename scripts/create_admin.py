from app import create_app, db
from models import User

app = create_app()

with app.app_context():
    # hapus admin lama
    old = User.query.filter_by(username='admin_smart').first()
    if old:
        db.session.delete(old)
        db.session.commit()

    new_admin = User(
        username='admin_smart',
        nama_lengkap='Super Admin Umu',
        email='admin@umu.ac.id',
        prodi='Umum',
        role='admin',
        nim='9999999999'
    )
    new_admin.password = 'AdminPass123'
    db.session.add(new_admin)
    db.session.commit()

    print("Admin dibuat!")
