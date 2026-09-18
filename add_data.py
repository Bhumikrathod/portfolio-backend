import requests

BASE = "http://127.0.0.1:5000/api"

# Pehle login karke token lo
login_res = requests.post(f"{BASE}/admin/login", json={"password": "Bhumika@123"})
token = login_res.json().get('token')

if not token:
    print("Login fail ho gaya! Password check karo.")
    exit()

headers = {"X-Admin-Token": token}

skills = [
    {"category": "Languages", "name": "Python"},
    {"category": "Languages", "name": "JavaScript"},
    {"category": "Languages", "name": "SQL"},
    {"category": "Languages", "name": "HTML5"},
    {"category": "Languages", "name": "CSS3"},
    {"category": "Frontend", "name": "React.js"},
    {"category": "Frontend", "name": "Bootstrap"},
    {"category": "Backend & Data", "name": "Node.js"},
    {"category": "Backend & Data", "name": "REST APIs"},
    {"category": "Backend & Data", "name": "MySQL"},
    {"category": "Backend & Data", "name": "MongoDB"},
    {"category": "Tools", "name": "Git"},
    {"category": "Tools", "name": "GitHub"},
]

experience = [
    {
        "role": "Full Stack Developer Intern",
        "company": "Cyberathon Technology Pvt Ltd",
        "duration": "Internship",
        "points": [
            "Developed and maintained web application features across frontend (HTML, CSS, JavaScript, React) and backend (Python, REST APIs) layers.",
            "Built and integrated database-driven modules using MySQL and MongoDB.",
            "Collaborated with the development team to deliver functional web applications following best practices.",
            "Worked with cross-functional teams to gather requirements and provide data-driven solutions."
        ]
    }
]

certifications = [
    {"title": "Project Management with Zoho", "issuer": "Reliance Foundation Skilling Academy (Online)", "link": ""},
    {"title": "Web Development Fundamentals (HTML, CSS, JavaScript)", "issuer": "Self-paced Online Course", "link": ""}
]

print("Adding skills...")
for s in skills:
    r = requests.post(f"{BASE}/skills", json=s, headers=headers)
    print(r.json())

print("\nAdding experience...")
for e in experience:
    r = requests.post(f"{BASE}/experience", json=e, headers=headers)
    print(r.json())

print("\nAdding certifications...")
for c in certifications:
    r = requests.post(f"{BASE}/certifications", json=c, headers=headers)
    print(r.json())

print("\nDone!")