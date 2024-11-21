from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

class Student(db.Model):
    student_id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    major = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'login' in request.form:
            # Xử lý đăng nhập
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect(url_for('dashboard'))
            else:
                flash('Đăng nhập thất bại. Vui lòng kiểm tra lại tên đăng nhập và mật khẩu.', 'danger')
        elif 'register' in request.form:
            # Xử lý đăng ký
            username = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            if password != confirm_password:
                flash('Mật khẩu không khớp. Vui lòng thử lại.', 'danger')
                return render_template('index.html')

            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Đăng ký thành công. Vui lòng đăng nhập.', 'success')
                return render_template('index.html')
            except:
                flash('Lỗi! Tên đăng nhập đã tồn tại.', 'danger')
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        students = Student.query.all()
        return render_template('dashboard.html', students=students)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        student_id = request.form['student_id']
        name = request.form['name']
        age = request.form['age']
        major = request.form['major']

        new_student = Student(student_id=student_id, name=name, age=age, major=major)
        try:
            db.session.add(new_student)
            db.session.commit()
            flash('Sinh viên đã được thêm thành công.', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()  # Đảm bảo quay lại trạng thái trước khi commit nếu gặp lỗi
            flash(f'Lỗi! Không thể thêm sinh viên. {str(e)}', 'danger')
    return render_template('add.html')

@app.route('/edit/<string:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.age = request.form['age']
        student.major = request.form['major']
        try:
            db.session.commit()
            flash('Cập nhật thông tin sinh viên thành công.', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Lỗi! Không thể cập nhật thông tin sinh viên. {str(e)}', 'danger')
    return render_template('edit.html', student=student)

@app.route('/delete/<string:student_id>')
def delete_student(student_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    student = Student.query.get_or_404(student_id)
    try:
        db.session.delete(student)
        db.session.commit()
        flash('Xóa sinh viên thành công.', 'success')
        return redirect(url_for('dashboard'))
    except Exception as e:
        db.session.rollback()
        flash(f'Lỗi! Không thể xóa sinh viên. {str(e)}', 'danger')
        return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
