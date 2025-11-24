#!/usr/bin/env python3
"""Barcha HTML templatelarni yaratish"""

import os

templates = {
    # 1. Tasks (Topshiriqlar)
    'tasks.html': '''{% extends "base.html" %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h2>📋 Topshiriqlar</h2>
        <div class="float-end">
            {% if current_user.role in ['admin', 'rahbar'] %}
            <a href="{{ url_for('task_new') }}" class="btn btn-primary">➕ Yangi Topshiriq</a>
            {% endif %}
        </div>
    </div>
</div>

<div class="row mt-4">
    <div class="col-12">
        <div class="card">
            <div class="card-body">
                <table class="table">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Nomi</th>
                            <th>Biriktirilgan</th>
                            <th>Muddat</th>
                            <th>Status</th>
                            <th>Prioritet</th>
                            <th>Amallar</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for task in tasks %}
                        <tr>
                            <td>{{ task.id }}</td>
                            <td>{{ task.title }}</td>
                            <td>{{ task.assigned_user.full_name if task.assigned_user else '-' }}</td>
                            <td>
                                <span class="badge bg-{{ task.get_urgency_color() }}">
                                    {{ task.due_date.strftime('%d.%m.%Y') if task.due_date else '-' }}
                                </span>
                            </td>
                            <td>
                                <span class="badge bg-info">{{ task.status }}</span>
                            </td>
                            <td>{{ task.priority }}</td>
                            <td>
                                <a href="{{ url_for('task_edit', id=task.id) }}" class="btn btn-sm btn-warning">Tahrirlash</a>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    # 2. Vehicles
    'vehicles.html': '''{% extends "base.html" %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h2>🚗 Avto Transport</h2>
        <div class="float-end">
            {% if current_user.role in ['admin', 'rahbar'] %}
            <a href="{{ url_for('vehicle_new') }}" class="btn btn-primary">➕ Yangi Transport</a>
            {% endif %}
        </div>
    </div>
</div>

<div class="row mt-4">
    {% for vehicle in vehicles %}
    <div class="col-md-4 mb-3">
        <div class="card">
            <div class="card-body">
                <h5>{{ vehicle.brand }} {{ vehicle.model }}</h5>
                <p><strong>Davlat raqami:</strong> {{ vehicle.plate_number }}</p>
                <p><strong>Yili:</strong> {{ vehicle.year }}</p>
                <p><strong>Haydovchi:</strong> {{ vehicle.driver_name or '-' }}</p>
                <p><strong>Probeg:</strong> {{ vehicle.mileage or '-' }} km</p>
                <a href="{{ url_for('vehicle_edit', id=vehicle.id) }}" class="btn btn-sm btn-primary">Tahrirlash</a>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}''',

    # 3. Ijro
    'ijro.html': '''{% extends "base.html" %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h2>📊 Ijro Moduli</h2>
        <p class="text-muted">Real-time topshiriqlar va chat</p>
    </div>
</div>

<div class="row mt-4">
    <div class="col-12">
        <div class="card">
            <div class="card-body">
                <div class="row">
                    {% for task in tasks %}
                    <div class="col-md-6 mb-3">
                        <div class="card border-{{ task.get_urgency_color() }}">
                            <div class="card-body">
                                <div class="d-flex justify-content-between">
                                    <h5>{{ task.title }}</h5>
                                    <span class="status-indicator status-{{ task.get_urgency_color() }}"></span>
                                </div>
                                <p>{{ task.description[:100] }}...</p>
                                <p><strong>Muddat:</strong> {{ task.due_date.strftime('%d.%m.%Y') if task.due_date else '-' }}</p>
                                <p><strong>Qolgan kunlar:</strong> {{ task.get_days_remaining() or '-' }}</p>
                                <a href="{{ url_for('ijro_detail', id=task.id) }}" class="btn btn-sm btn-info">Ko'rish</a>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    # 4. Buildings
    'buildings.html': '''{% extends "base.html" %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h2>🏢 Binolar</h2>
        <div class="float-end">
            <a href="{{ url_for('building_new') }}" class="btn btn-primary">➕ Yangi Bino</a>
        </div>
    </div>
</div>

<div class="row mt-4">
    {% for building in buildings %}
    <div class="col-md-4 mb-3">
        <div class="card">
            <div class="card-body">
                <h5>{{ building.name }}</h5>
                <p><strong>Kategoriya:</strong> {{ building.category or '-' }}</p>
                <p><strong>Manzil:</strong> {{ building.address or '-' }}</p>
                <p><strong>Maydon:</strong> {{ building.area or '-' }} m²</p>
                <p><strong>Qavatlar:</strong> {{ building.floors or '-' }}</p>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}''',

    # 5. Green Spaces
    'green_spaces.html': '''{% extends "base.html" %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h2>🌳 Yashil Makonlar</h2>
        <div class="float-end">
            <a href="{{ url_for('green_space_new') }}" class="btn btn-success">➕ Yangi Makon</a>
        </div>
    </div>
</div>

<div class="row mt-4">
    {% for space in spaces %}
    <div class="col-md-4 mb-3">
        <div class="card">
            <div class="card-body">
                <h5>{{ space.name }}</h5>
                <p><strong>Kategoriya:</strong> {{ space.category or '-' }}</p>
                <p><strong>Joylashuv:</strong> {{ space.location or '-' }}</p>
                <p><strong>Maydon:</strong> {{ space.area or '-' }} m²</p>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}''',

    # 6. Solar Panels
    'solar_panels.html': '''{% extends "base.html" %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h2>☀️ Quyosh Panellari</h2>
        <div class="float-end">
            <a href="{{ url_for('solar_panel_new') }}" class="btn btn-warning">➕ Yangi Panel</a>
        </div>
    </div>
</div>

<div class="row mt-4">
    {% for panel in panels %}
    <div class="col-md-4 mb-3">
        <div class="card">
            <div class="card-body">
                <h5>Panel #{{ panel.id }}</h5>
                <p><strong>Bino:</strong> {{ panel.building.name if panel.building else '-' }}</p>
                <p><strong>Panel soni:</strong> {{ panel.panel_count or '-' }}</p>
                <p><strong>Quvvat:</strong> {{ panel.total_capacity or '-' }} kW</p>
                <p><strong>Ishlab chiqaruvchi:</strong> {{ panel.manufacturer or '-' }}</p>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}''',

    # 7. Employees
    'employees.html': '''{% extends "base.html" %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h2>👥 Xodimlar</h2>
        <div class="float-end">
            {% if current_user.role in ['admin', 'rahbar'] %}
            <a href="{{ url_for('employee_new') }}" class="btn btn-primary">➕ Yangi Xodim</a>
            {% endif %}
        </div>
    </div>
</div>

<div class="row mt-4">
    {% for employee in employees %}
    <div class="col-md-4 mb-3">
        <div class="card">
            <div class="card-body">
                <h5>{{ employee.full_name }}</h5>
                <p><strong>Lavozim:</strong> {{ employee.position or '-' }}</p>
                <p><strong>Bo'lim:</strong> {{ employee.department or '-' }}</p>
                <p><strong>Telefon:</strong> {{ employee.phone or '-' }}</p>
                <p><strong>Email:</strong> {{ employee.email or '-' }}</p>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}''',

    # 8. Outsourcing
    'outsourcing.html': '''{% extends "base.html" %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h2>🤝 Autsorsing Xizmatlari</h2>
    </div>
</div>

<div class="row mt-4">
    {% for service in services %}
    <div class="col-md-6 mb-3">
        <div class="card">
            <div class="card-body">
                <h5>{{ service.service_name }}</h5>
                <p><strong>Turi:</strong> {{ service.service_type or '-' }}</p>
                <p><strong>Provayder:</strong> {{ service.provider_name or '-' }}</p>
                <p><strong>Shartnoma:</strong> {{ service.contract_number or '-' }}</p>
                <p><strong>Summa:</strong> {{ service.contract_amount or '-' }}</p>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}''',

    # 9. Organizations
    'organizations.html': '''{% extends "base.html" %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h2>🏛️ Tashkilotlar</h2>
    </div>
</div>

<div class="row mt-4">
    {% for org in organizations %}
    <div class="col-md-4 mb-3">
        <div class="card">
            <div class="card-body">
                <h5>{{ org.name }}</h5>
                <p><strong>Xodimlar:</strong> {{ org.employee_count or '-' }}</p>
                <p><strong>Bino hajmi:</strong> {{ org.building_size or '-' }} m²</p>
                <p><strong>Telefon:</strong> {{ org.phone or '-' }}</p>
                <p><strong>Email:</strong> {{ org.email or '-' }}</p>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}''',

    # 10. Guests
    'guests.html': '''{% extends "base.html" %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h2>🤵 Mehmonlar</h2>
    </div>
</div>

<div class="row mt-4">
    <div class="col-12">
        <table class="table">
            <thead>
                <tr>
                    <th>F.I.O</th>
                    <th>Tashkilot</th>
                    <th>Kelgan sana</th>
                    <th>Sabab</th>
                </tr>
            </thead>
            <tbody>
                {% for guest in guests %}
                <tr>
                    <td>{{ guest.full_name }}</td>
                    <td>{{ guest.organization or '-' }}</td>
                    <td>{{ guest.visit_date.strftime('%d.%m.%Y') if guest.visit_date else '-' }}</td>
                    <td>{{ guest.visit_reason or '-' }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}''',

    # 11. Congratulations
    'congratulations.html': '''{% extends "base.html" %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h2>🎉 Tabriknomalar</h2>
    </div>
</div>

<div class="row mt-4">
    {% for congrat in congratulations %}
    <div class="col-md-6 mb-3">
        <div class="card">
            <div class="card-body">
                <h5>{{ congrat.occasion }}</h5>
                <p><strong>Kimga:</strong> {{ congrat.recipient_name }}</p>
                <p><strong>Sana:</strong> {{ congrat.date.strftime('%d.%m.%Y') if congrat.date else '-' }}</p>
                <p><strong>Sovg'a:</strong> {{ congrat.gift_description or '-' }}</p>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}''',

    # 12. Contracts
    'contracts.html': '''{% extends "base.html" %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h2>📄 Shartnomalar</h2>
    </div>
</div>

<div class="row mt-4">
    <div class="col-12">
        <table class="table">
            <thead>
                <tr>
                    <th>Raqam</th>
                    <th>Firma</th>
                    <th>Sana</th>
                    <th>Summa</th>
                    <th>Status</th>
                    <th>To'lov</th>
                </tr>
            </thead>
            <tbody>
                {% for contract in contracts %}
                <tr>
                    <td>{{ contract.contract_number }}</td>
                    <td>{{ contract.company_name }}</td>
                    <td>{{ contract.contract_date.strftime('%d.%m.%Y') if contract.contract_date else '-' }}</td>
                    <td>{{ contract.contract_amount or '-' }}</td>
                    <td><span class="badge bg-info">{{ contract.status }}</span></td>
                    <td><span class="badge bg-success">{{ contract.payment_status or '-' }}</span></td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}''',

    # 13. Warehouse
    'warehouse.html': '''{% extends "base.html" %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h2>📦 Ombor So'rovnomalari</h2>
        <div class="float-end">
            <a href="{{ url_for('warehouse_new') }}" class="btn btn-primary">➕ Yangi So'rovnoma</a>
        </div>
    </div>
</div>

<div class="row mt-4">
    <div class="col-12">
        <table class="table">
            <thead>
                <tr>
                    <th>Raqam</th>
                    <th>Sana</th>
                    <th>Bo'lim</th>
                    <th>Status</th>
                    <th>So'rovchi</th>
                </tr>
            </thead>
            <tbody>
                {% for req in requests %}
                <tr>
                    <td>{{ req.request_number }}</td>
                    <td>{{ req.request_date.strftime('%d.%m.%Y') if req.request_date else '-' }}</td>
                    <td>{{ req.department or '-' }}</td>
                    <td><span class="badge bg-warning">{{ req.status }}</span></td>
                    <td>{{ req.requested_by.full_name if req.requested_by else '-' }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}'''
}

# Templatelarni yaratish
for filename, content in templates.items():
    filepath = f'templates/{filename}'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ {filename}")

print(f"\n🎉 {len(templates)} ta template yaratildi!")
