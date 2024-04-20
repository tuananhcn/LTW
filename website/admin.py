from flask import Blueprint, render_template, request, session, flash, redirect, url_for
import sqlite3
admin = Blueprint("admin", __name__)

sqldbname = 'LAPTRINHWEB.db'
def admin_required(f):
    def decorated_function(*args, **kwargs):
      if 'current_user' not in session or 'quyen' not in session['current_user'] or session['current_user']['quyen'] != 1:
          flash("You must log in as an admin to access this page", "error")
          return redirect(url_for('admin.login'))
      return f(*args, **kwargs)
    return decorated_function
def get_obj_user(username,password):
    result =[]
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    sqlcommand = "Select * from user where email =? and password = ?"
    cur.execute(sqlcommand,(username,password))
    obj_user = cur.fetchone()
    if obj_user:
        result = obj_user
    conn.close()
    return result;
@admin.route('/')
@admin_required
def index():
  conn = sqlite3.connect(sqldbname)
  cursor = conn.cursor()
  sqlcommand = ("SELECT * FROM FASHION")
  cursor.execute(sqlcommand)
  storages = cursor.fetchall()
  conn.close()
  return render_template('admin/dashboard.html', storages=storages)
@admin.route('/users')

def Users():
  conn = sqlite3.connect(sqldbname)
  cursor = conn.cursor()
  sqlcommand = ("SELECT * FROM user")
  cursor.execute(sqlcommand)
  storages = cursor.fetchall()
  conn.close()
  return render_template('admin/users.html', storages=storages)
@admin.route('/users/add', methods=['GET','POST'])

def addUser():
  if request.method == 'POST':
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    quyen = request.form['quyen']
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user (name, email, password, quyen) VALUES(?,?,?,?)", (name, email, password, quyen))
    conn.commit()
    conn.close()
    flash("You have added successfully", "success")
    return redirect(url_for('admin.Users'))
  return render_template('admin/addUser.html')
@admin.route('/add', methods=['GET','POST'])

def add():
  if request.method == 'POST':
    product = request.form['Product']
    brand = request.form['Brand']
    rating = request.form['Rating']
    model = request.form['Model']
    picture = request.form['Picture']
    price = request.form['Price']
    details = request.form['Details']
    
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO FASHION (product, brand, rating, model, picture, price, details) VALUES(?,?,?,?,?,?,?)", (product, brand, rating, model, picture, price, details))
    conn.commit()
    conn.close()
    flash("You have added successfully", "success")
    return redirect("/admin")
  return render_template('admin/add.html')
@admin.route('/edit/<int:id>', methods=['GET', 'POST'])

def edit_product(id):
  conn = sqlite3.connect(sqldbname)
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM FASHION where id = ?", (id,))
  storage = cursor.fetchone()
  conn.close()
  if request.method == 'POST':
    product = request.form['Product']
    brand = request.form['Brand']
    rating = request.form['Rating']
    model = request.form['Model']
    picture = request.form['Picture']
    price = request.form['Price']
    details = request.form['Details']
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    cursor.execute("Update FASHION set product = ?, brand = ?, rating = ?, model = ?, picture = ?, price = ?, details = ? where id = ?", (product, brand, rating, model, picture, price, details, id))
    conn.commit()
    conn.close()
    flash("Product updated successfully!", "success")
    return redirect("/admin")
  return render_template("admin/edit.html", storage=storage)
@admin.route('/users/edit/<int:id>', methods=['GET', 'POST'])

def edit_user(id):
  conn = sqlite3.connect(sqldbname)
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM user where user_id = ?", (id,))
  storage = cursor.fetchone()
  conn.close()
  if request.method == 'POST':
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    quyen = request.form['quyen']
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    cursor.execute("Update user set name = ?, email = ?, password = ?, quyen = ? where user_id = ?", (name, email, password, quyen, id))
    conn.commit()
    conn.close()
    flash("User updated successfully!", "success")
    return redirect(url_for("admin.Users"))
  return render_template("admin/editUser.html", storage=storage)
@admin.route('/delete/<int:id>', methods=['POST'])

def delete(id):
  conn = sqlite3.connect(sqldbname)
  cursor = conn.cursor()
  cursor.execute("DELETE FROM FASHION WHERE id = ?", (id,))
  conn.commit()
  conn.close()
  flash("You have successfully deleted the item", "success")
  return redirect("/admin")
@admin.route('/users/delete/<int:id>', methods=['POST'])

def deleteUser(id):
  conn = sqlite3.connect(sqldbname)
  cursor = conn.cursor()
  cursor.execute("DELETE FROM user WHERE user_id = ?", (id,))
  conn.commit()
  conn.close()
  flash("You have successfully deleted user", "success")
  return redirect(url_for('admin.Users'))
@admin.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['txt_username']
        password = request.form['txt_password']
        obj_user = get_obj_user(username,password)
        if obj_user:
            obj_user ={
                "user_id" : obj_user[0],
                "name": obj_user[1],
                "email":obj_user[2],
                "quyen": obj_user[4]
            }
            session['current_user'] = obj_user
            print(session['current_user'])
            if session['current_user']['quyen'] != 1:
              flash("You have to be admin to log in this page", "error")
              return redirect(url_for('admin.login'))
            flash("You have log in successfully", "success")
            return redirect(url_for("admin.Users"))
        flash("Please check your username and password", 'error')
        return redirect(url_for('admin.login'))
        
    return render_template('admin/login.html')
@admin.route('/logout')
def logout():
    # Remove the user's data from the session
    session.pop('current_user', None)
    # Redirect to the login page or any other desired page
    return redirect(url_for('admin.login'))