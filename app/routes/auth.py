from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import add_user, get_user_by_username
from app.forms import LoginForm, RegistrationForm

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_username(form.username.data)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        flash('Geçersiz kullanıcı adı veya şifre', 'danger')
    return render_template('auth/login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        if get_user_by_username(form.username.data):
            flash('Bu kullanıcı adı zaten kullanılıyor', 'danger')
            return render_template('auth/register.html', form=form)
        
        user = add_user(form.username.data, form.email.data, form.password.data)
        login_user(user)
        flash('Hesabınız başarıyla oluşturuldu!', 'success')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Başarıyla çıkış yaptınız', 'success')
    return redirect(url_for('auth.login')) 