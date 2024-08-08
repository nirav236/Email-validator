from flask import Flask, render_template, request, jsonify, redirect, url_for
import re
import dns.resolver
import smtplib
import json

app = Flask(__name__)

def is_valid_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None

def is_valid_domain(email):
    domain = email.split('@')[1]
    try:
        dns.resolver.resolve(domain, 'MX')
        return True
    except dns.resolver.NXDOMAIN:
        return False
    except dns.resolver.NoAnswer:
        return False
    except dns.resolver.NoNameservers:
        return False

def is_active_email(email):
    domain = email.split('@')[1]
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_record = str(mx_records[0].exchange)
        server = smtplib.SMTP()
        server.set_debuglevel(0)
        server.connect(mx_record)
        server.helo(server.local_hostname)
        server.mail('test@example.com')
        code, _ = server.rcpt(email)
        server.quit()
        return code == 250
    except Exception:
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate-single-email', methods=['POST'])
def validate_single_email():
    email = request.form['email']
    result = {
        'email': email,
        'format': is_valid_email(email),
        'domain': False,
        'active': False
    }
    if result['format']:
        result['domain'] = is_valid_domain(email)
        if result['domain']:
            result['active'] = is_active_email(email)
    return jsonify(result)

@app.route('/results')
def results():
    data = request.args.get('data', '')
    try:
        results = json.loads(data)  # Safely convert the JSON string to a list of dictionaries
    except json.JSONDecodeError:
        results = []  # Handle the case where data is not a valid JSON string

    return render_template('results.html', results=results)

if __name__ == "__main__":
    app.run(debug=True)
    
    
