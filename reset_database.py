"""
AF IMPERIYA - DATABASE RESET
Database'ni to'liq qayta yaratish va yangilash
"""

import os
import sys
import shutil

print("="*60)
print("  AF IMPERIYA - DATABASE RESET")
print("="*60)
print()

# 1. Eski database'ni o'chirish
if os.path.exists('instance'):
    try:
        print("[1/3] Eski database o'chirilmoqda...")
        shutil.rmtree('instance')
        print("      ✅ Eski database o'chirildi!")
        print()
    except Exception as e:
        print(f"      ⚠️  Ogohlantirish: {e}")
        print()

# 2. Yangi instance folder yaratish
if not os.path.exists('instance'):
    os.makedirs('instance')
    print("[2/3] Instance folder yaratildi ✅")
    print()

# 3. App'ni import qilish va database yaratish
print("[3/3] Database yaratilmoqda...")
try:
    from app import app, db, User
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("      ✅ Barcha table'lar yaratildi!")
        
        # Verify tables
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"      ✅ Yaratilgan table'lar soni: {len(tables)}")
        
        # Check if tasks table has deadline column
        if 'tasks' in tables:
            columns = [col['name'] for col in inspector.get_columns('tasks')]
            if 'deadline' in columns:
                print("      ✅ tasks.deadline column mavjud!")
            else:
                print("      ❌ tasks.deadline column YO'Q!")
        
        # Create admin user
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@af-imperiya.uz',
                full_name='Administrator',
                role='admin',
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            print("      ✅ Admin user yaratildi")
        
        # Create rahbar user
        rahbar = User.query.filter_by(username='rahbar').first()
        if not rahbar:
            rahbar = User(
                username='rahbar',
                email='rahbar@af-imperiya.uz',
                full_name='Rahbar',
                role='rahbar',
                is_active=True
            )
            rahbar.set_password('rahbar123')
            db.session.add(rahbar)
            print("      ✅ Rahbar user yaratildi")
        
        # Create test user
        test_user = User.query.filter_by(username='user').first()
        if not test_user:
            test_user = User(
                username='user',
                email='user@af-imperiya.uz',
                full_name='Test User',
                role='user',
                is_active=True
            )
            test_user.set_password('user123')
            db.session.add(test_user)
            print("      ✅ Test user yaratildi")
        
        # Commit
        db.session.commit()
        print("      ✅ Database commit qilindi")
        
        # Final verification
        user_count = User.query.count()
        print(f"      ✅ Jami userlar: {user_count}")
        
        print()
        print("="*60)
        print("  🎉 DATABASE MUVAFFAQIYATLI YARATILDI!")
        print("="*60)
        print()
        print("Default users:")
        print("  👤 admin   / admin123  - Administrator")
        print("  👤 rahbar  / rahbar123 - Rahbar")
        print("  👤 user    / user123   - Test User")
        print()
        print("="*60)
        
except Exception as e:
    print(f"      ❌ XATOLIK: {e}")
    import traceback
    traceback.print_exc()
    print()
    print("YECHIM:")
    print("1. Virtual environment faol ekanligini tekshiring")
    print("2. Barcha kutubxonalar o'rnatilganligini tekshiring")
    print("3. Qaytadan urinib ko'ring")
    sys.exit(1)
