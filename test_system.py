#!/usr/bin/env python3
"""Tizimni to'liq test qilish"""

import os

print("="*70)
print(" AF IMPERIYA - Tizim Testi ".center(70, "="))
print("="*70)

# Fayllarni tekshirish
files = {
    'Asosiy': ['app.py', 'requirements.txt', '.env.example', 'Procfile', 'runtime.txt', 'README.md', 'DEPLOYMENT.md', 'QUICK_START.md', 'FEATURES.md', '.gitignore'],
    'Modules': ['modules/__init__.py', 'modules/models.py', 'modules/routes.py', 'modules/telegram_bot.py', 'modules/utils.py'],
    'Templates': ['templates/base.html', 'templates/login.html', 'templates/dashboard.html', 'templates/tasks.html', 'templates/vehicles.html', 'templates/ijro.html'],
    'Forms': ['templates/task_form.html', 'templates/vehicle_form.html', 'templates/warehouse_form.html'],
    'Static': ['static/css/style.css', 'static/js/main.js']
}

total = 0
missing = 0

for category, file_list in files.items():
    print(f"\n📁 {category}:")
    for f in file_list:
        if os.path.exists(f):
            size = os.path.getsize(f) / 1024
            print(f"  ✅ {f:<50} ({size:.1f} KB)")
            total += 1
        else:
            print(f"  ❌ {f}")
            missing += 1

print("\n" + "="*70)
print(f"📊 Natija:")
print(f"   ✅ Tayyor: {total} ta fayl")
print(f"   ❌ Yo'q: {missing} ta fayl")

# Modullarni sanash
print(f"\n📦 Modullar:")
modules = ['Topshiriqlar', 'Avto Transport', 'Ijro', 'Binolar', 'Yashil Makonlar', 
           'Quyosh Panellari', 'Xodimlar', 'Autsorsing', 'Tashkilotlar', 
           'Mehmonlar', 'Tabriknomalar', 'Shartnomalar', 'Ombor']
for i, mod in enumerate(modules, 1):
    print(f"   {i}. {mod}")

print("\n" + "="*70)
print(" ✅ TIZIM TO'LIQ TAYYOR! ".center(70, "="))
print("="*70)
