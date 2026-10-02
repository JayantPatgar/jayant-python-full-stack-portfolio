import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "development-secret-key")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.String(300))
    github_url = db.Column(db.String(300))
    live_url = db.Column(db.String(300))
    image = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100))


@app.context_processor
def global_data():
    return {
        "site_name": "Jayant Krishna Patgar",
        "current_year": datetime.now().year,
    }


@app.route("/")
def home():
    projects = Project.query.order_by(Project.id.desc()).limit(3).all()
    skills = Skill.query.order_by(Skill.id.asc()).all()
    return render_template("index.html", projects=projects, skills=skills)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/skills")
def skills():
    skills_data = Skill.query.order_by(Skill.id.asc()).all()
    return render_template("skills.html", skills=skills_data)


@app.route("/projects")
def projects():
    projects_data = Project.query.order_by(Project.id.desc()).all()
    return render_template("projects.html", projects=projects_data)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    contact_message = None
    contact_status = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        subject = request.form.get("subject", "").strip()
        message_text = request.form.get("message", "").strip()

        if not name or not email or not subject or not message_text:
            contact_message = "Please fill in all fields."
            contact_status = "error"
        else:
            try:
                new_message = Message(
                    name=name,
                    email=email,
                    subject=subject,
                    message=message_text,
                )
                db.session.add(new_message)
                db.session.commit()
                contact_message = "✓ Message sent successfully! Thank you for contacting me."
                contact_status = "success"
            except Exception as error:
                db.session.rollback()
                print("Contact form error:", error)
                contact_message = "Unable to send your message. Please try again."
                contact_status = "error"

    return render_template(
        "contact.html",
        contact_message=contact_message,
        contact_status=contact_status,
    )


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    print("====================================")
    print("Jayant Portfolio is starting...")
    print("====================================")
    app.run(debug=True)
