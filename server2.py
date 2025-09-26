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

    def send_email(self, form_data):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = "nasreddinehamou8@gmail.com"
            msg['Subject'] = "Nouvelle demande d'appartement"

            # Parse the wilaya value to get just the name
            wilaya_full = form_data.get('wilaya', '')
            wilaya_name = wilaya_full.split('|')[1] if '|' in wilaya_full else wilaya_full

            body = f"""
            Nouvelle demande d'appartement reçue:

            Email: {form_data.get('email', '')}
            Nom et Prénom: {form_data.get('prenom', '')}
            Téléphone: {form_data.get('telephone', '')}
            Wilaya: {wilaya_name.strip()}
            Profession: {form_data.get('profession', '')}
            Type d'Appartement: {form_data.get('appartement', '')}

            Date de soumission: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """

            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)

            text = msg.as_string()
            server.sendmail(self.sender_email, "nasreddinehamou8@gmail.com", text)
            server.quit()
            return True, "Message envoyé avec succès!"

        except Exception as e:
            return False, f"Erreur d'envoi: {str(e)}"

class ContactFormHandler(CORSRequestHandler):
    def __init__(self, *args, **kwargs):
        self.email_handler = EmailHandler(
            sender_email="nasreddinehamou8@gmail.com",  # Your email
            sender_password="rqfzuhtmmxqcduvg"    # Your app password
        )
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == '/send_email_apartment':
            try:
                # Get content length
                content_length = int(self.headers['Content-Length'])
                # Read the POST data
                post_data = self.rfile.read(content_length).decode('utf-8')
                # Parse the form data
                form_data = dict(urllib.parse.parse_qs(post_data))

                # Convert lists to single values
                form_data = {k: v[0] for k, v in form_data.items()}

                # Send email
                success, message = self.email_handler.send_email(form_data)

                # Prepare response
                response = {
                    'success': success,
                    'message': message
                }

                # Send response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())

            except Exception as e:
                response = {
                    'success': False,
                    'message': str(e)
                }
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, ContactFormHandler)
    print(f"Server running on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()