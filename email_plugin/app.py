from flask import Flask, request, jsonify,send_file
from flask_cors import CORS
from dotenv import load_dotenv
import os, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import decode_header
import logging
import imaplib
import email
from datetime import datetime 


# Set up logging
load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}},supports_credentials=True)

@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response

@app.route("/dify-plugin/hello", methods=["POST"])
def hello_plugin():
    data = request.json
    name = data.get("name", "stranger")
    return jsonify({
"message": f"Hello, {name}! This is a response from your Dify plugin."
})
@app.route("/send_email", methods=["POST", "OPTIONS"])
def send_email():
    if request.method == "OPTIONS":
        return '', 200  # Required for CORS preflight

    data = request.json
    if not data:
        logging.warning("No JSON body received.")
        return jsonify({"error": "Missing JSON body"}), 400

    msg = MIMEMultipart()
    msg['Subject'] = data['subject']
    msg['From'] = os.getenv("SMTP_FROM_EMAIL")
    msg['To'] = data['to']

    recipients = [data["to"]]
    if data.get("cc"):
        msg['Cc'] = data['cc']
        recipients += [email.strip() for email in data["cc"].split(",") if email.strip()]
    if data.get("bcc"):
        msg['Bcc'] = data['bcc']
        recipients += [email.strip() for email in data["bcc"].split(",") if email.strip()]

    msg.attach(MIMEText(data['body'], "html"))

    if "attachments" in data:
        for file_path in data["attachments"]:
            try:
                with open(file_path, "rb") as f:
                    part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
                    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                    msg.attach(part)
            except Exception as e:
                return jsonify({"error": f"Attachment error: {str(e)}"}), 400

    try:
        logging.info("Recipients: %s", recipients)
        server = smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT")))
        server.starttls()
        server.login(os.getenv("SMTP_USERNAME"), os.getenv("SMTP_PASSWORD"))
        server.sendmail(os.getenv("SMTP_FROM_EMAIL"), recipients, msg.as_string())
        server.quit()
        logging.info("Email sent successfully")
        return jsonify({"message": "Email sent successfully"})
    except Exception as e:
        logging.error("SMTP Error: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route("/openapi.yaml", methods=["GET"])
def serve_openapi():
    return send_file("openapi.yaml", mimetype="text/yaml")

@app.route("/openapi_receive.yaml", methods=["GET"])
def serve_openapi_receive():
    return send_file("openapi_receive.yaml", mimetype="text/yaml")

def decode_mime_words(s):
    decoded = decode_header(s)
    return ''.join([
        part.decode(enc or 'utf-8') if isinstance(part, bytes) else part
        for part, enc in decoded
    ])    
# @app.route("/check_email",methods=["GET", "OPTIONS"])
# def check_email():
#     try:
#         imap_host = os.getenv("IMAP_HOST")
#         imap_port = int(os.getenv("IMAP_PORT"))
#         username = os.getenv("IMAP_USERNAME")
#         password = os.getenv("IMAP_PASSWORD")

#         mail = imaplib.IMAP4_SSL(imap_host, imap_port)
#         mail.login(username, password)
#         mail.select("Inbox")

#         _, messages = mail.search(None, "UNSEEN") 
#         email_ids = messages[0].split()

#         new_emails = []

#         for eid in email_ids:
#             _, msg_data = mail.fetch(eid, "(RFC822)")
#             raw_email = msg_data[0][1]
#             msg = email.message_from_bytes(raw_email)

#             subject = decode_mime_words(msg["Subject"] or "No Subject")
#             from_ = decode_mime_words(msg.get("From", "Unknown Sender"))

            
#             body = ""
#             attachments = []
#             if msg.is_multipart():
#                 for part in msg.walk():
#                     content_type = part.get_content_type()
#                     disposition = part.get("Content-Disposition", "")

#                     if content_type == "text/plain" and "attachment" not in disposition:
#                         body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
#                     elif "attachment" in disposition:
#                         filename = part.get_filename()
#                         if filename:
#                             attachments.append(decode_mime_words(filename))
#             else:
#                 body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")

#             new_emails.append({
#                 "from": from_,
#                 "subject": subject,
#                 "body": body.strip(),
#                 "attachments": attachments
#             })

#         mail.logout()

#         return jsonify({
#             "unread_count": len(new_emails),
#             "emails": new_emails
#         })
#     except Exception as e:
#         logging.exception("Error checking email:")
#         return jsonify({"error": str(e)}), 500
@app.route("/check_email", methods=["GET", "OPTIONS"])
def check_email():
    try:
        # Get credentials from .env
        imap_host = os.getenv("IMAP_HOST")
        imap_port = int(os.getenv("IMAP_PORT"))
        username = os.getenv("IMAP_USERNAME")
        password = os.getenv("IMAP_PASSWORD")

        # Connect to IMAP server
        imap = imaplib.IMAP4_SSL(imap_host, imap_port)
        imap.login(username, password)
        imap.select("INBOX")

        # Search unread emails from today
        today = datetime.today().strftime('%d-%b-%Y')
        _, messages = imap.search(None, f'(UNSEEN SINCE "{today}")')
        email_ids = messages[0].split()

        new_emails = []

        for eid in email_ids:
            _, msg_data = imap.fetch(eid, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject = decode_mime_words(msg["Subject"] or "No Subject")
            from_ = decode_mime_words(msg.get("From", "Unknown Sender"))
            body = ""
            attachments = []

            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    disposition = part.get("Content-Disposition", "")
                    if content_type == "text/plain" and "attachment" not in disposition:
                        body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                    elif "attachment" in disposition:
                        filename = part.get_filename()
                        if filename:
                            attachments.append(decode_mime_words(filename))
            else:
                body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")

            new_emails.append({
                "from": from_,
                "subject": subject,
                "body": body.strip(),
                "attachments": attachments
            })

        imap.logout()

        return jsonify({
            "unread_count": len(new_emails),
            "emails": new_emails
        })

    except Exception as e:
        import logging
        logging.exception("❌ Error checking email:")
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(port=5003,debug=True)

