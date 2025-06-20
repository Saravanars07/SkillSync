from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "secretkey"

# Temporary in-memory storage
posted_projects = []

@app.route('/')
def home():
    return render_template('index.html', projects=posted_projects)

@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email and password:
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials!", "danger")
    return render_template('student_login.html')

@app.route('/startup/post', methods=['GET', 'POST'])
def post_project():
    if request.method == 'POST':
        project = {
            'title': request.form['title'],
            'skills': request.form['skills'],
            'duration': request.form['duration'],
            'description': request.form['description']
        }
        posted_projects.append(project)
        flash("Project posted successfully!", "success")
        return redirect(url_for('home'))
    return render_template('post_project.html')

if __name__ == '__main__':
    app.run(debug=True)
