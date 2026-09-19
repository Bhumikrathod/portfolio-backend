from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
from config import Config
from models import db, Project, Message, Skill, Experience, Certification, Testimonial, SocialLink, Video
from flask_mail import Mail, Message as MailMessage

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
mail = Mail(app)
CORS(app)

with app.app_context():
    db.create_all()


def require_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('X-Admin-Token')
        if token != app.config['ADMIN_SECRET']:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated


@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    if data.get('password') == app.config['ADMIN_PASSWORD']:
        return jsonify({'token': app.config['ADMIN_SECRET']})
    return jsonify({'error': 'Invalid password'}), 401


# ---------- PROJECTS ----------

@app.route('/api/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([p.to_dict() for p in projects])

@app.route('/api/projects', methods=['POST'])
@require_admin
def create_project():
    data = request.get_json()
    new_project = Project(
        title=data['title'],
        description=data['description'],
        link=data.get('link', ''),
        image_link=data.get('image_link', '')
    )
    db.session.add(new_project)
    db.session.commit()
    return jsonify(new_project.to_dict()), 201

@app.route('/api/projects/<int:id>', methods=['PUT'])
@require_admin
def update_project(id):
    project = Project.query.get_or_404(id)
    data = request.get_json()
    project.title = data.get('title', project.title)
    project.description = data.get('description', project.description)
    project.link = data.get('link', project.link)
    project.image_link = data.get('image_link', project.image_link)
    db.session.commit()
    return jsonify(project.to_dict())

@app.route('/api/projects/<int:id>', methods=['DELETE'])
@require_admin
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Project deleted'})


# ---------- SKILLS ----------

@app.route('/api/skills', methods=['GET'])
def get_skills():
    skills = Skill.query.all()
    return jsonify([s.to_dict() for s in skills])

@app.route('/api/skills', methods=['POST'])
@require_admin
def create_skill():
    data = request.get_json()
    new_skill = Skill(category=data['category'], name=data['name'])
    db.session.add(new_skill)
    db.session.commit()
    return jsonify(new_skill.to_dict()), 201

@app.route('/api/skills/<int:id>', methods=['PUT'])
@require_admin
def update_skill(id):
    skill = Skill.query.get_or_404(id)
    data = request.get_json()
    skill.category = data.get('category', skill.category)
    skill.name = data.get('name', skill.name)
    db.session.commit()
    return jsonify(skill.to_dict())

@app.route('/api/skills/<int:id>', methods=['DELETE'])
@require_admin
def delete_skill(id):
    skill = Skill.query.get_or_404(id)
    db.session.delete(skill)
    db.session.commit()
    return jsonify({'message': 'Skill deleted'})


# ---------- EXPERIENCE ----------

@app.route('/api/experience', methods=['GET'])
def get_experience():
    exp = Experience.query.all()
    return jsonify([e.to_dict() for e in exp])

@app.route('/api/experience', methods=['POST'])
@require_admin
def create_experience():
    data = request.get_json()
    points_str = '||'.join(data.get('points', []))
    new_exp = Experience(role=data['role'], company=data['company'], duration=data.get('duration', ''), points=points_str)
    db.session.add(new_exp)
    db.session.commit()
    return jsonify(new_exp.to_dict()), 201

@app.route('/api/experience/<int:id>', methods=['PUT'])
@require_admin
def update_experience(id):
    exp = Experience.query.get_or_404(id)
    data = request.get_json()
    exp.role = data.get('role', exp.role)
    exp.company = data.get('company', exp.company)
    exp.duration = data.get('duration', exp.duration)
    if 'points' in data:
        exp.points = '||'.join(data['points'])
    db.session.commit()
    return jsonify(exp.to_dict())

@app.route('/api/experience/<int:id>', methods=['DELETE'])
@require_admin
def delete_experience(id):
    exp = Experience.query.get_or_404(id)
    db.session.delete(exp)
    db.session.commit()
    return jsonify({'message': 'Experience deleted'})


# ---------- CERTIFICATIONS ----------

@app.route('/api/certifications', methods=['GET'])
def get_certifications():
    certs = Certification.query.all()
    return jsonify([c.to_dict() for c in certs])

@app.route('/api/certifications', methods=['POST'])
@require_admin
def create_certification():
    data = request.get_json()
    new_cert = Certification(title=data['title'], issuer=data['issuer'], link=data.get('link', ''))
    db.session.add(new_cert)
    db.session.commit()
    return jsonify(new_cert.to_dict()), 201

@app.route('/api/certifications/<int:id>', methods=['PUT'])
@require_admin
def update_certification(id):
    cert = Certification.query.get_or_404(id)
    data = request.get_json()
    cert.title = data.get('title', cert.title)
    cert.issuer = data.get('issuer', cert.issuer)
    cert.link = data.get('link', cert.link)
    db.session.commit()
    return jsonify(cert.to_dict())

@app.route('/api/certifications/<int:id>', methods=['DELETE'])
@require_admin
def delete_certification(id):
    cert = Certification.query.get_or_404(id)
    db.session.delete(cert)
    db.session.commit()
    return jsonify({'message': 'Certification deleted'})


# ---------- TESTIMONIALS ----------

@app.route('/api/testimonials', methods=['GET'])
def get_testimonials():
    items = Testimonial.query.all()
    return jsonify([t.to_dict() for t in items])

@app.route('/api/testimonials', methods=['POST'])
@require_admin
def create_testimonial():
    data = request.get_json()
    new_item = Testimonial(name=data['name'], role=data.get('role', ''), message=data['message'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.to_dict()), 201

@app.route('/api/testimonials/<int:id>', methods=['PUT'])
@require_admin
def update_testimonial(id):
    item = Testimonial.query.get_or_404(id)
    data = request.get_json()
    item.name = data.get('name', item.name)
    item.role = data.get('role', item.role)
    item.message = data.get('message', item.message)
    db.session.commit()
    return jsonify(item.to_dict())

@app.route('/api/testimonials/<int:id>', methods=['DELETE'])
@require_admin
def delete_testimonial(id):
    item = Testimonial.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Testimonial deleted'})


# ---------- MESSAGES ----------

@app.route('/api/messages', methods=['GET'])
@require_admin
def get_messages():
    messages = Message.query.all()
    return jsonify([m.to_dict() for m in messages])

@app.route('/api/messages/<int:id>', methods=['DELETE'])
@require_admin
def delete_message(id):
    msg = Message.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    return jsonify({'message': 'Message deleted'})


# ---------- CONTACT ----------

@app.route('/api/contact', methods=['POST'])
def create_message():
    data = request.get_json()
    new_msg = Message(name=data['name'], email=data['email'], message=data['message'])
    db.session.add(new_msg)
    db.session.commit()

    try:
        email_notif = MailMessage(
            subject=f"New Portfolio Message from {data['name']}",
            sender=app.config['MAIL_USERNAME'],
            recipients=[app.config['MAIL_USERNAME']],
            body=f"Name: {data['name']}\nEmail: {data['email']}\n\nMessage:\n{data['message']}"
        )
        mail.send(email_notif)
    except Exception as e:
        print("Email sending failed:", e)

    return jsonify({'message': 'Message sent successfully'}), 201


# ---------- SOCIAL LINKS ----------

@app.route('/api/social-links', methods=['GET'])
def get_social_links():
    links = SocialLink.query.all()
    return jsonify([l.to_dict() for l in links])

@app.route('/api/social-links', methods=['POST'])
@require_admin
def create_social_link():
    data = request.get_json()
    new_link = SocialLink(platform=data['platform'], url=data['url'])
    db.session.add(new_link)
    db.session.commit()
    return jsonify(new_link.to_dict()), 201

@app.route('/api/social-links/<int:id>', methods=['PUT'])
@require_admin
def update_social_link(id):
    link = SocialLink.query.get_or_404(id)
    data = request.get_json()
    link.platform = data.get('platform', link.platform)
    link.url = data.get('url', link.url)
    db.session.commit()
    return jsonify(link.to_dict())

@app.route('/api/social-links/<int:id>', methods=['DELETE'])
@require_admin
def delete_social_link(id):
    link = SocialLink.query.get_or_404(id)
    db.session.delete(link)
    db.session.commit()
    return jsonify({'message': 'Social link deleted'})

# ---------- VIDEOS ----------

# ---------- VIDEOS ----------

@app.route('/api/videos', methods=['GET'])
def get_videos():
    videos = Video.query.all()
    return jsonify([v.to_dict() for v in videos])

@app.route('/api/videos', methods=['POST'])
@require_admin
def create_video():
    data = request.get_json()
    new_video = Video(
        title=data['title'],
        platform=data['platform'],
        url=data['url'],
        thumbnail_url=data.get('thumbnail_url', '')
    )
    db.session.add(new_video)
    db.session.commit()
    return jsonify(new_video.to_dict()), 201

@app.route('/api/videos/<int:id>', methods=['PUT'])
@require_admin
def update_video(id):
    video = Video.query.get_or_404(id)
    data = request.get_json()
    video.title = data.get('title', video.title)
    video.platform = data.get('platform', video.platform)
    video.url = data.get('url', video.url)
    video.thumbnail_url = data.get('thumbnail_url', video.thumbnail_url)
    db.session.commit()
    return jsonify(video.to_dict())

@app.route('/api/videos/<int:id>', methods=['DELETE'])
@require_admin
def delete_video(id):
    video = Video.query.get_or_404(id)
    db.session.delete(video)
    db.session.commit()
    return jsonify({'message': 'Video deleted'})

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)