"""
AF IMPERIYA - Database Models (YANGILANGAN)
Barcha ma'lumotlar bazasi modellari + Fayl yuklash
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """Foydalanuvchi modeli"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(200))
    role = db.Column(db.String(20), nullable=False, index=True)
    
    # Telegram integration
    telegram_id = db.Column(db.String(100))
    telegram_chat_id = db.Column(db.String(50))
    telegram_username = db.Column(db.String(100))
    telegram_notifications = db.Column(db.Boolean, default=True)
    
    phone = db.Column(db.String(20))
    position = db.Column(db.String(100))
    department = db.Column(db.String(100))
    birth_date = db.Column(db.Date)
    hire_date = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def has_module_access(self, module_name):
        if self.role in ['admin', 'rahbar']:
            return True
        return db.session.query(UserModule).filter_by(
            user_id=self.id, module_name=module_name, is_active=True
        ).first() is not None
    
    def __repr__(self):
        return f'<User {self.username}>'


class Task(db.Model):
    """Topshiriqlar modeli"""
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20), default='medium')
    status = db.Column(db.String(20), default='pending', index=True)
    deadline = db.Column(db.DateTime)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    category = db.Column(db.String(50))
    tags = db.Column(db.String(200))
    progress = db.Column(db.Integer, default=0)
    estimated_hours = db.Column(db.Float)
    actual_hours = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    created_by = db.relationship('User', foreign_keys=[created_by_id], backref='created_tasks')
    assigned_to = db.relationship('User', foreign_keys=[assigned_to_id], backref='assigned_tasks')
    
    def __repr__(self):
        return f'<Task {self.title}>'


class Vehicle(db.Model):
    """Avto transport modeli - YANGILANGAN"""
    __tablename__ = 'vehicles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(50))
    model = db.Column(db.String(50))
    year = db.Column(db.Integer)
    plate_number = db.Column(db.String(20), unique=True)
    vin_number = db.Column(db.String(50))
    color = db.Column(db.String(30))
    fuel_type = db.Column(db.String(20))
    category = db.Column(db.String(50))
    driver_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))
    mileage = db.Column(db.Integer)
    status = db.Column(db.String(20), default='active')
    
    # YANGI: Fayl yuklash
    photo_path = db.Column(db.String(255))  # Rasm
    documents_path = db.Column(db.String(255))  # PDF hujjatlar
    
    purchase_date = db.Column(db.Date)
    purchase_price = db.Column(db.Float)
    insurance_expiry = db.Column(db.Date)
    technical_inspection_date = db.Column(db.Date)
    notes = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    driver = db.relationship('User', backref='vehicles')
    organization = db.relationship('Organization', backref='vehicles')
    
    def __repr__(self):
        return f'<Vehicle {self.name}>'


class Building(db.Model):
    """Binolar modeli - YANGILANGAN"""
    __tablename__ = 'buildings'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(300))
    category = db.Column(db.String(50))
    area = db.Column(db.Float)
    volume = db.Column(db.Float)
    floors = db.Column(db.Integer)
    rooms = db.Column(db.Integer)
    construction_year = db.Column(db.Integer)
    
    # YANGI: Fayl yuklash
    photo_path = db.Column(db.String(255))  # Rasm
    documents_path = db.Column(db.String(255))  # PDF hujjatlar
    blueprint_path = db.Column(db.String(255))  # Loyiha
    
    cadastral_number = db.Column(db.String(50))
    owner = db.Column(db.String(200))
    purpose = db.Column(db.String(100))
    condition = db.Column(db.String(50))
    estimated_value = db.Column(db.Float)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Building {self.name}>'


class GreenSpace(db.Model):
    """Yashil makonlar modeli - YANGILANGAN"""
    __tablename__ = 'green_spaces'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    
    # YANGI: Binoga bog'lash
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), index=True)
    
    category = db.Column(db.String(50))
    area = db.Column(db.Float)
    location = db.Column(db.String(300))
    plant_types = db.Column(db.Text)
    tree_count = db.Column(db.Integer)
    shrub_count = db.Column(db.Integer)
    flower_count = db.Column(db.Integer)
    lawn_area = db.Column(db.Float)
    irrigation_system = db.Column(db.String(100))
    maintenance_schedule = db.Column(db.String(100))
    last_maintenance_date = db.Column(db.Date)
    next_maintenance_date = db.Column(db.Date)
    responsible_person = db.Column(db.String(200))
    notes = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    building = db.relationship('Building', backref='green_spaces')
    
    def __repr__(self):
        return f'<GreenSpace {self.name}>'


class SolarPanel(db.Model):
    """Quyosh panellari modeli - YANGILANGAN"""
    __tablename__ = 'solar_panels'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'))
    capacity_kw = db.Column(db.Float)
    panel_count = db.Column(db.Integer)
    brand = db.Column(db.String(100))
    model = db.Column(db.String(100))
    installation_date = db.Column(db.Date)
    
    # YANGI: API integratsiya
    api_endpoint = db.Column(db.String(500))  # Tashqi API URL
    api_key = db.Column(db.String(200))  # API kalit
    last_sync = db.Column(db.DateTime)  # Oxirgi sinxronizatsiya
    
    # Real-time ma'lumotlar
    current_production = db.Column(db.Float)  # Joriy ishlab chiqarish (kW)
    daily_production = db.Column(db.Float)  # Kunlik (kWh)
    monthly_production = db.Column(db.Float)  # Oylik (kWh)
    yearly_production = db.Column(db.Float)  # Yillik (kWh)
    total_production = db.Column(db.Float)  # Umumiy (kWh)
    
    efficiency = db.Column(db.Float)
    warranty_expiry = db.Column(db.Date)
    maintenance_cost = db.Column(db.Float)
    notes = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    building = db.relationship('Building', backref='solar_panels')
    
    def __repr__(self):
        return f'<SolarPanel {self.name}>'


class Employee(db.Model):
    """Xodimlar modeli - YANGILANGAN"""
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    employee_number = db.Column(db.String(50), unique=True)
    full_name = db.Column(db.String(200), nullable=False)
    position = db.Column(db.String(100))
    department = db.Column(db.String(100))
    hire_date = db.Column(db.Date)
    birth_date = db.Column(db.Date)
    passport_number = db.Column(db.String(50))
    passport_issued_date = db.Column(db.Date)
    passport_issued_by = db.Column(db.String(200))
    address = db.Column(db.Text)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    
    # YANGI: Fayl yuklash
    photo_path = db.Column(db.String(255))  # Rasm
    passport_file = db.Column(db.String(255))  # Pasport PDF
    resume_file = db.Column(db.String(255))  # Rezume Word/PDF
    contract_file = db.Column(db.String(255))  # Shartnoma
    
    education = db.Column(db.String(200))
    experience_years = db.Column(db.Integer)
    skills = db.Column(db.Text)
    salary = db.Column(db.Float)
    status = db.Column(db.String(20), default='active')
    notes = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', backref='employee_profile')
    
    def __repr__(self):
        return f'<Employee {self.full_name}>'


class Outsourcing(db.Model):
    """Autsorsing modeli - YANGILANGAN"""
    __tablename__ = 'outsourcing'
    
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(200), nullable=False)
    
    # YANGI: To'liq ma'lumotlar
    contract_number = db.Column(db.String(100))
    contract_date = db.Column(db.Date, nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    amount = db.Column(db.Float)
    contact_person = db.Column(db.String(200))
    contact_phone = db.Column(db.String(20))
    contact_email = db.Column(db.String(120))
    
    company_name = db.Column(db.String(200))
    service_type = db.Column(db.String(100))
    frequency = db.Column(db.String(50))
    cost = db.Column(db.Float)
    payment_terms = db.Column(db.String(100))
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Outsourcing {self.service_name}>'


class Organization(db.Model):
    """Tashkilotlar modeli - YANGILANGAN"""
    __tablename__ = 'organizations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    
    # YANGI: Fayl yuklash
    logo_path = db.Column(db.String(255))
    documents_path = db.Column(db.String(255))  # PDF/Excel
    certificates_path = db.Column(db.String(255))
    
    tin = db.Column(db.String(50))
    address = db.Column(db.Text)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    website = db.Column(db.String(200))
    director = db.Column(db.String(200))
    contact_person = db.Column(db.String(200))
    bank_account = db.Column(db.String(100))
    bank_name = db.Column(db.String(200))
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Organization {self.name}>'


class Guest(db.Model):
    """Mehmonlar modeli - YANGILANGAN"""
    __tablename__ = 'guests'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200), nullable=False)
    organization = db.Column(db.String(200))
    position = db.Column(db.String(100))
    visit_date = db.Column(db.DateTime, nullable=False)
    visit_purpose = db.Column(db.String(300))
    
    # YANGI: Fayl yuklash
    photo_path = db.Column(db.String(255))
    documents_path = db.Column(db.String(255))  # Word/Excel/PDF
    
    passport_number = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    host_name = db.Column(db.String(200))
    host_department = db.Column(db.String(100))
    services_provided = db.Column(db.Text)
    notes = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Guest {self.full_name}>'


class Congratulation(db.Model):
    """Tabriknomalar modeli - YANGILANGAN"""
    __tablename__ = 'congratulations'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # YANGI: Kategoriya
    category = db.Column(db.String(50), nullable=False)  # Tug'ilgan kun, Bayram, Yutuq, va h.k.
    
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    occasion = db.Column(db.String(200))
    date = db.Column(db.Date, nullable=False)
    
    # YANGI: To'liq ma'lumotlar
    recipient_name = db.Column(db.String(200))  # Kimga
    gift_description = db.Column(db.String(300))  # Nima berildi
    amount = db.Column(db.Float)  # Summa
    
    # YANGI: Fayl yuklash
    photo_path = db.Column(db.String(255))
    certificate_path = db.Column(db.String(255))  # PDF
    
    message = db.Column(db.Text)
    sent_by = db.Column(db.String(200))
    notes = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    employee = db.relationship('Employee', backref='congratulations')
    
    def __repr__(self):
        return f'<Congratulation {self.occasion}>'


class Contract(db.Model):
    """Shartnomalar modeli - YANGILANGAN"""
    __tablename__ = 'contracts'
    
    id = db.Column(db.Integer, primary_key=True)
    contract_number = db.Column(db.String(100), unique=True, nullable=False)
    
    # YANGI: Xodim tanlashi
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    company_name = db.Column(db.String(200), nullable=False)
    contract_type = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    amount = db.Column(db.Float)
    currency = db.Column(db.String(10), default='UZS')
    status = db.Column(db.String(20), default='active')
    payment_terms = db.Column(db.String(200))
    description = db.Column(db.Text)
    file_path = db.Column(db.String(255))
    notes = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    created_by = db.relationship('User', backref='contracts')
    
    def __repr__(self):
        return f'<Contract {self.contract_number}>'


class WarehouseRequest(db.Model):
    """Ombor so'rovnomalari modeli - YANGILANGAN"""
    __tablename__ = 'warehouse_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    request_number = db.Column(db.String(100), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # YANGI: To'liq ma'lumotlar
    department = db.Column(db.String(100))
    request_date = db.Column(db.Date, nullable=False)
    needed_date = db.Column(db.Date)
    
    items = db.Column(db.Text)
    quantity = db.Column(db.String(100))
    unit = db.Column(db.String(50))
    purpose = db.Column(db.String(300))
    
    # Umumiy ma'lumotlar
    total_items = db.Column(db.Integer)
    estimated_cost = db.Column(db.Float)
    priority = db.Column(db.String(20), default='normal')
    
    status = db.Column(db.String(20), default='pending')
    approved_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    approval_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    file_path = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', foreign_keys=[user_id], backref='warehouse_requests')
    approved_by = db.relationship('User', foreign_keys=[approved_by_id])
    
    def __repr__(self):
        return f'<WarehouseRequest {self.request_number}>'


# Qo'shimcha modellar
class TaskComment(db.Model):
    """Topshiriq izohlar"""
    __tablename__ = 'task_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    task = db.relationship('Task', backref='comments')
    user = db.relationship('User', backref='task_comments')


class TaskCollaborator(db.Model):
    """Topshiriq hamkorlar"""
    __tablename__ = 'task_collaborators'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.String(50))
    added_at = db.Column(db.DateTime, default=datetime.utcnow)


class SystemLog(db.Model):
    """Tizim loglari"""
    __tablename__ = 'system_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(100), nullable=False)
    module = db.Column(db.String(50))
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    user = db.relationship('User', backref='logs')


class UserModule(db.Model):
    """Foydalanuvchi modullari"""
    __tablename__ = 'user_modules'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    module_name = db.Column(db.String(50), nullable=False)
    can_create = db.Column(db.Boolean, default=False)
    can_edit = db.Column(db.Boolean, default=False)
    can_delete = db.Column(db.Boolean, default=False)
    can_view = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='modules')


class ChatMessage(db.Model):
    """Admin bilan xodim o'rtasida chat"""
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Modul context
    module_name = db.Column(db.String(50))
    module_item_id = db.Column(db.Integer)
    
    # Kim kimga
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Xabar
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')
    
    def __repr__(self):
        return f'<ChatMessage from {self.sender.username}>'
