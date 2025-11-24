"""
AF IMPERIYA - Database Initialization
Database'ni yaratish va default ma'lumotlarni qo'shish
"""

import os
import sys

# Instance papkasini yaratish
if not os.path.exists('instance'):
    os.makedirs('instance')
    print("✅ Instance folder created")

# App'ni import qilish
try:
    from app import app, db, User
    print("✅ App imported successfully")
except Exception as e:
    print(f"❌ Error importing app: {e}")
    sys.exit(1)

# Database yaratish
try:
    with app.app_context():
        # Drop all (faqat development uchun!)
        # db.drop_all()
        
        # Create all tables
        db.create_all()
        print("✅ Database tables created")
        
        # Check if admin exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            # Create admin
            admin = User(
                username='admin',
                email='admin@af-imperiya.uz',
                full_name='Administrator',
                role='admin',
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            print("✅ Admin user created")
        else:
            print("ℹ️  Admin user already exists")
        
        # Check if rahbar exists
        rahbar = User.query.filter_by(username='rahbar').first()
        if not rahbar:
            # Create rahbar
            rahbar = User(
                username='rahbar',
                email='rahbar@af-imperiya.uz',
                full_name='Rahbar',
                role='rahbar',
                is_active=True
            )
            rahbar.set_password('rahbar123')
            db.session.add(rahbar)
            print("✅ Rahbar user created")
        else:
            print("ℹ️  Rahbar user already exists")
        
        # Commit
        db.session.commit()
        print("✅ Database committed")
        
        # Verify
        user_count = User.query.count()
        print(f"✅ Total users in database: {user_count}")
        
        print("\n" + "="*60)
        print("🎉 DATABASE INITIALIZATION COMPLETE!")
        print("="*60)
        print("\nDefault users:")
        print("  👤 Username: admin    | Password: admin123 | Role: admin")
        print("  👤 Username: rahbar   | Password: rahbar123 | Role: rahbar")
        print("\n" + "="*60)
        
except Exception as e:
    print(f"❌ Error creating database: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
