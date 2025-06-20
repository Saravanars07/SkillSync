from flask import Flask, render_template, request, redirect, url_for, flash, session
import os

port = int(os.environ.get("PORT", 5000))
app = Flask(__name__)
app.secret_key = "secretkey"

# In-memory store (replace with database in real app)
posted_projects = []
project_id_counter = 1

@app.route('/')
def home():
    return render_template('index.html', projects=posted_projects)

@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email and password:
            session['logged_in'] = True
            session['user_type'] = 'student'
            flash("Student logged in!", "success")
            return redirect(url_for('home'))
    return render_template('student_login.html')

@app.route('/startup/post', methods=['GET', 'POST'])
def post_project():
    global project_id_counter
    if not session.get('logged_in') or session.get('user_type') != 'student':
        flash("Login required", "danger")
        return redirect(url_for('student_login'))

    if request.method == 'POST':
        project = {
            'id': project_id_counter,
            'title': request.form['title'],
            'skills': request.form['skills'],
            'duration': request.form['duration'],
            'description': request.form['description']
        }
        posted_projects.append(project)
        project_id_counter += 1
        flash("Project posted successfully!", "success")
        return redirect(url_for('home'))
    return render_template('post_project.html')


@app.route('/project/edit/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    project = next((p for p in posted_projects if p['id'] == id), None)
    if not project:
        flash("Project not found", "danger")
        return redirect(url_for('home'))

    if request.method == 'POST':
        project['title'] = request.form['title']
        project['skills'] = request.form['skills']
        project['duration'] = request.form['duration']
        project['description'] = request.form['description']
        flash("Project updated successfully!", "success")
        return redirect(url_for('home'))

    return render_template('edit_project.html', project=project)


@app.route('/project/delete/<int:id>')
def delete_project(id):
    global posted_projects
    posted_projects = [p for p in posted_projects if p['id'] != id]
    flash("Project deleted successfully!", "info")
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out", "info")
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=port)
