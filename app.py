from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

app = Flask(__name__)

# Set sender email and password (consider using environment variables for security)
SENDER_EMAIL = "amitguptaie99@gmail.com"
SENDER_PASSWORD = "unvj phdt qjuw jhyg"  # Replace with secure method of handling passwords

def send_email(recipient_email, message_body):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg['Subject'] = "No Subject"
    msg.attach(MIMEText(message_body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def analyze_message(message):
    abusive_words = [
        "abuse", "hate", "violence", "kill", "fight", "attack", "hurt", 
        "rage", "aggressive", "assault", "danger", "threat", "hostile", 
        "anger", "stupid", "idiot", "fool", "dumb", "jerk", "worthless", 
        "loser", "shut up", "moron", "hate you", "weapon", "blood", 
        "gun", "knife"
    ]
    for word in abusive_words:
        if word in message.lower():
            return False
    return True

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def handle_email():
    data = request.json
    recipient_email = data['recipient_email']
    message_body = data['message_body']

    if analyze_message(message_body):
        success = send_email(recipient_email, message_body)
        return jsonify({'success': success})
    else:
        return jsonify({'success': False, 'error': 'Message contains abusive content.'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Get the port from environment or default to 5000
    app.run(debug=True, host='0.0.0.0', port=port)
