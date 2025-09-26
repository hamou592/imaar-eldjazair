import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import urllib.parse
from datetime import datetime

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

class EmailHandler:
    def __init__(self, sender_email, sender_password):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def send_general_email(self, recipient, subject, message, sender_name):
        try:
            msg = MIMEMultipart()
            msg['From'] = f"{sender_name} <{self.sender_email}>"
            msg['To'] = recipient
            msg['Subject'] = "Demande D'Information"

            body = f"""
Salut, 

Nom: {sender_name}
Email: {self.sender_email}
Message:
{message}

Merci

Date de soumission: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)

            server.sendmail(self.sender_email, recipient, msg.as_string())
            server.quit()
            return True, "Email sent successfully!"

        except Exception as e:
            return False, f"Failed to send email: {str(e)}"

    def send_apartment_email(self, form_data):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = "nasreddinehamou8@gmail.com"
            msg['Subject'] = "Nouvelle Demande Pour La Résidence Orion"

            wilaya_full = form_data.get('wilaya', '')
            wilaya_name = wilaya_full.split('|')[1] if '|' in wilaya_full else wilaya_full

            body = f"""
Salut,

Email: {form_data.get('email', '')}
Nom et Prénom: {form_data.get('prenom', '')}
Téléphone: {form_data.get('telephone', '')}
Wilaya: {wilaya_name.strip()}
Profession: {form_data.get('profession', '')}
Type d'Appartement: {form_data.get('appartement', '')}

Merci

Date de soumission: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)

            server.sendmail(self.sender_email, msg['To'], msg.as_string())
            server.quit()
            return True, "Message envoyé avec succès!"

        except Exception as e:
            return False, f"Erreur d'envoi: {str(e)}"

    def send_whatsapp_email(self, form_data):
        # You can customize this method if you want different email content or subject
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = "nasreddinehamou8@gmail.com"
            msg['Subject'] = "Nouvelle Demande Pour La Résidence RUBIS"

            wilaya_full = form_data.get('wilaya', '')
            wilaya_name = wilaya_full.split('|')[1] if '|' in wilaya_full else wilaya_full

            body = f"""
Salut,

Email: {form_data.get('email', '')}
Nom et Prénom: {form_data.get('prenom', '')} {form_data.get('nom', '')}
Téléphone: {form_data.get('telephone', '')}
Wilaya: {wilaya_name.strip()}
Profession: {form_data.get('profession', '')}
Type d'Appartement: {form_data.get('appartement', '')}

Merci

Date de soumission: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)

            server.sendmail(self.sender_email, msg['To'], msg.as_string())
            server.quit()
            return True, "Message WhatsApp envoyé avec succès!"

        except Exception as e:
            return False, f"Erreur d'envoi WhatsApp: {str(e)}"

class UnifiedRequestHandler(CORSRequestHandler):
    def __init__(self, *args, **kwargs):
        self.email_handler = EmailHandler(
            sender_email="nasreddinehamou8@gmail.com",  # Your email
            sender_password="rqfzuhtmmxqcduvg"          # Your app password
        )
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        form_data = dict(urllib.parse.parse_qs(post_data))
        form_data = {k: v[0] for k, v in form_data.items()}

        if self.path == '/send_email':
            name = form_data.get('name', '')
            email = form_data.get('email', '')
            subject = form_data.get('subject', '')
            message = form_data.get('message', '')

            success, msg = self.email_handler.send_general_email(
                recipient="nasreddinehamou8@gmail.com",
                subject=subject,
                message=message,
                sender_name=name
            )
            self.respond_json(success, msg)

        elif self.path == '/send_email_apartment':
            success, msg = self.email_handler.send_apartment_email(form_data)
            self.respond_json(success, msg)

        elif self.path == '/send_email_whatsapp':
            success, msg = self.email_handler.send_whatsapp_email(form_data)
            self.respond_json(success, msg)

        else:
            self.send_response(404)
            self.end_headers()

    def respond_json(self, success, message):
        response = {
            'success': success,
            'message': message
        }
        self.send_response(200 if success else 500)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, UnifiedRequestHandler)
    print(f"Server running on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()