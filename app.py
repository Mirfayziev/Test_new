from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime
import os

# ============================================================
# FLASK APP
# ============================================================
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "AF_IMPERIYA_SECRET")

# ============================================================
# DATABASE CONNECTION (NEON/RENDER + LOCAL SUPPORT)
# ============================================================
if os.getenv("DATABASE_URL"):
    db_url = os.getenv("DATABASE_URL")
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///instance/af_imperiya.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ============================================================
# INIT DB & LOGIN MANAGER
# ============================================================
from modules.models import db, User
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# ============================================================
# JINJA HELPERS
# ============================================================
def format_money(value):
    """Simple money formatter for dashboard."""
    try:
        value = float(value)
    except Exception:
        return value
    return f"{value:,.0f}".replace(",", " ")

app.jinja_env.globals["format_money"] = format_money

# ============================================================
# AUTH ROUTES (LOGIN, REGISTER, LOGOUT)
# ============================================================
@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            # last_login ixtiyoriy
            try:
                user.last_login = datetime.now()
                db.session.commit()
            except Exception:
                db.session.rollback()
            return redirect(url_for("dashboard"))

        flash("Login yoki parol noto‘g‘ri!", "danger")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        username = request.form.get("username")
        email = request.form.get("email")
        telegram_username = request.form.get("telegram_username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # validation
        if password != confirm_password:
            flash("Parollar mos emas!", "danger")
            return redirect(url_for("register"))

        if User.query.filter_by(username=username).first():
            flash("Bu username band!", "danger")
            return redirect(url_for("register"))

        if User.query.filter_by(email=email).first():
            flash("Bu email band!", "danger")
            return redirect(url_for("register"))

        # create user
        user = User(
            username=username,
            email=email,
            full_name=full_name,
            telegram_username=telegram_username,
            role="user",
            is_active=True
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Ro‘yxatdan o‘tish muvaffaqiyatli! Endi login qiling.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# ============================================================
# DASHBOARD
# ============================================================
@app.route("/dashboard")
@login_required
def dashboard():
    from modules.models import Task

    tasks = Task.query.all()
    total_tasks = len(tasks)
    pending = len([t for t in tasks if t.status == "pending"])
    in_progress = len([t for t in tasks if t.status == "in_progress"])
    completed = len([t for t in tasks if t.status == "completed"])
    overdue = len([
        t for t in tasks
        if t.deadline and t.deadline < datetime.now() and t.status != "completed"
    ])

    stats = {
        "total_tasks": total_tasks,
        "pending": pending,
        "in_progress": in_progress,
        "completed": completed,
        "overdue": overdue,

        # aliases for new dashboard template
        "completed_tasks": completed,
        "overdue_tasks": overdue,

        # optional money stat (you can replace later with real sum)
        "total_amount": 0
    }

    return render_template(
        "dashboard.html",
        user=current_user,
        stats=stats
    )

# ============================================================
# PROFILE ROUTES (base.html va profile.html uchun)
# ============================================================
@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@app.route("/profile/update", methods=["POST"])
@login_required
def profile_update():
    user = current_user
    user.full_name = request.form.get("full_name")
    user.email = request.form.get("email")
    user.phone = request.form.get("phone")
    user.telegram_username = request.form.get("telegram_username")

    # checkbox bo'lsa "on" bo'ladi, bo'lmasa None
    user.telegram_notifications = (request.form.get("telegram_notifications") == "on")

    try:
        db.session.commit()
        flash("Profil muvaffaqiyatli yangilandi!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Xatolik: {e}", "danger")

    return redirect(url_for("profile"))


@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirm_new = request.form.get("confirm_new_password")

        if not current_user.check_password(old_password):
            flash("Eski parol noto‘g‘ri!", "danger")
            return redirect(url_for("change_password"))

        if new_password != confirm_new:
            flash("Yangi parollar mos emas!", "danger")
            return redirect(url_for("change_password"))

        current_user.set_password(new_password)
        try:
            db.session.commit()
            flash("Parol yangilandi!", "success")
            return redirect(url_for("profile"))
        except Exception as e:
            db.session.rollback()
            flash(f"Xatolik: {e}", "danger")

    return render_template("change_password.html")


# ============================================================
# ADMIN ROUTES
# ============================================================
@app.route("/admin/dashboard")
@login_required
def admin_dashboard():
    if current_user.role != "admin":
        flash("Ruxsat yo‘q!", "danger")
        return redirect(url_for("dashboard"))

    users = User.query.all()
    stats = {
        "total": len(users),
        "active": len([u for u in users if u.is_active]),
        "admins": len([u for u in users if u.role == "admin"])
    }

    return render_template("admin/dashboard.html", stats=stats)


@app.route("/admin/users")
@login_required
def admin_users():
    if current_user.role != "admin":
        flash("Ruxsat yo‘q!", "danger")
        return redirect(url_for("dashboard"))

    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", users=users)


@app.route("/admin/users/new", methods=["GET", "POST"])
@login_required
def admin_user_new():
    if current_user.role != "admin":
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        full_name = request.form.get("full_name")
        phone = request.form.get("phone")
        role = request.form.get("role")
        password = request.form.get("password")

        if User.query.filter_by(username=username).first():
            flash("Username band!", "danger")
            return redirect(url_for("admin_user_new"))

        user = User(
            username=username,
            email=email,
            full_name=full_name,
            phone=phone,
            role=role
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("User yaratildi!", "success")
        return redirect(url_for("admin_users"))

    return render_template("admin/user_form.html")


@app.route("/admin/users/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
def admin_user_edit(user_id):
    if current_user.role != "admin":
        return redirect(url_for("dashboard"))

    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        user.email = request.form.get("email")
        user.full_name = request.form.get("full_name")
        user.phone = request.form.get("phone")
        user.role = request.form.get("role")

        db.session.commit()
        flash("User o‘zgartirildi!", "success")
        return redirect(url_for("admin_users"))

    return render_template("admin/user_form.html", user=user)


@app.route("/admin/users/<int:user_id>/delete", methods=["POST"])
@login_required
def admin_user_delete(user_id):
    if current_user.role != "admin":
        return redirect(url_for("dashboard"))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    flash("User o‘chirildi!", "success")
    return redirect(url_for("admin_users"))


# ============================================================
# MODULE ROUTES (TASKS, IJRO, VEHICLES…)
# ============================================================
from modules.routes import init_routes
init_routes(app, db)


# ============================================================
# STATIC / FILE ROUTES
# ============================================================
@app.route("/uploads/<path:filename>")
def uploads(filename):
    return send_from_directory("uploads", filename)


# ===================== AUTO INIT DATABASE + ADMIN =====================
# Prod'da gunicorn import qilganda ham xavfsiz: admin bo'lmasa yaratadi
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username="admin").first():
        admin = User(
            username="admin",
            email="admin@gmail.com",
            full_name="Super Admin",
            role="admin",
            is_active=True
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("AUTO: Admin created!")


# ============================================================
# RUN (LOCAL)
# ============================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
