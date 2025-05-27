from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User, Task, Bid
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qnnotate_jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

ADMIN_USERNAME = 'gle63s'
ADMIN_PASSWORD = 'benzo_na_bimmer'

#@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return redirect(url_for('admin_login'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials')
    
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    tasks = Task.query.all()
    users = User.query.all()
    return render_template('admin_dashboard.html', tasks=tasks, users=users)

@app.route('/admin/create_user', methods=['GET', 'POST'])
def create_user():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
        else:
            hashed_password = generate_password_hash(password)
            user = User(username=username, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('User created successfully')
            return redirect(url_for('admin_dashboard'))
    
    return render_template('create_user.html')

@app.route('/admin/create_task', methods=['GET', 'POST'])
def create_task():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        
        task = Task(title=title, description=description)
        db.session.add(task)
        db.session.commit()
        flash('Task created successfully')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('create_task.html')

@app.route('/admin/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    task = Task.query.get_or_404(task_id)
    
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        db.session.commit()
        flash('Task updated successfully')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('edit_task.html', task=task)

@app.route('/admin/delete_task/<int:task_id>')
def delete_task(task_id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/task_details/<int:task_id>')
def admin_task_details(task_id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    task = Task.query.get_or_404(task_id)
    bids = Bid.query.filter_by(task_id=task_id).all()
    return render_template('task_details.html', task=task, bids=bids, is_admin=True)

@app.route('/admin/assign_task/<int:task_id>/<int:bid_id>')
def assign_task(task_id, bid_id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    task = Task.query.get_or_404(task_id)
    bid = Bid.query.get_or_404(bid_id)
    
    task.status = 'assigned'
    task.assigned_user_id = bid.user_id
    task.winning_bid_amount = bid.amount
    bid.is_selected = True
    
    db.session.commit()
    flash('Task assigned successfully')
    return redirect(url_for('admin_task_details', task_id=task_id))

@app.route('/admin/complete_task/<int:task_id>')
def complete_task(task_id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    task = Task.query.get_or_404(task_id)
    
    if task.status == 'assigned' and task.assigned_user_id:
        task.status = 'completed'
        user = User.query.get(task.assigned_user_id)
        user.total_earnings += task.winning_bid_amount
        db.session.commit()
        flash('Task marked as complete and payment added to user')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid credentials')
    
    return render_template('user_login.html')

@app.route('/user/dashboard')
def user_dashboard():
    if not session.get('user_id'):
        return redirect(url_for('user_login'))
    
    user = User.query.get(session['user_id'])
    tasks = Task.query.filter_by(status='open').all()
    user_bids = Bid.query.filter_by(user_id=user.id).all()
    
    return render_template('user_dashboard.html', user=user, tasks=tasks, user_bids=user_bids)

@app.route('/user/bid/<int:task_id>', methods=['POST'])
def place_bid(task_id):
    if not session.get('user_id'):
        return redirect(url_for('user_login'))
    
    user_id = session['user_id']
    amount = float(request.form['amount'])
    
    existing_bid = Bid.query.filter_by(user_id=user_id, task_id=task_id).first()
    
    if existing_bid:
        existing_bid.amount = amount
    else:
        bid = Bid(user_id=user_id, task_id=task_id, amount=amount)
        db.session.add(bid)
    
    db.session.commit()
    flash('Bid placed successfully')
    return redirect(url_for('user_dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    with app.app_context():
        create_tables() # ADDED THIS
    app.run(debug=True)