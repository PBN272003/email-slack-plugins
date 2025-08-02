# Email and Slack Integration Plugins

This project provides a straightforward way to connect email and Slack functionalities into your applications.

What this really means is you get two distinct plugins: one for handling emails and another for interacting with Slack.

---

## 🔧 Plugin Breakdown

- **Email Plugin**: A service that allows you to interact with Gmail using the SMTP and IMAP protocols.
- **Slack Plugin**: A service to interact with your Slack workspace.

Each plugin is built as a separate application, making it easy to use only the one you need.

---

## 📁 Repository Structure and File Information

- `email_plugin/`: Contains everything needed for the email service.
- `slack_plugin/`: Holds the files for the Slack integration.
- `app.py` and `slack_app.py`: These are the main Python files for each plugin.
- `.env`: Environment files that store secret keys and other configuration details. One for each plugin.
- `.yaml`: These files define the API for each plugin using the OpenAPI specification. They guide how the API works.
- `requirements.txt`: Lists all the Python packages you need to install.

---

## 🔐 .env File Content

### email_plugin/.env

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=XYZ@gmail.com
SMTP_PASSWORD=**** **** **** ****
SMTP_FROM_EMAIL=XYZ@gmail.com
SMTP_FROM_NAME=Priyank Naik
REMOTE_INSTALL_PORT=5003
REMOTE_INSTALL_KEY=*********************
IMAP_HOST=imap.gmail.com
IMAP_PORT=993
IMAP_USERNAME=XYZ@gmail.com
IMAP_PASSWORD=**** **** **** ****
```

### slack_plugin/.env
```env
SLACK_BOT_TOKEN=xoxb-*******************
REMOTE_INSTALL_PORT=5005
REMOTE_INSTALL_KEY=*********************
```

### Testing with Postman and ngrok
Here's the thing about testing a local web service: it's not accessible from the internet. That's where ngrok comes in.
ngrok creates a secure tunnel to your local machine, giving you a public URL that you can use to test your API from anywhere.

The images of how the dify and slack looks like:
My Custom Tools/Plugins
![custom_tools](https://github.com/user-attachments/assets/c3c49495-4c4b-4d6f-bb8a-eb4db6149e22)

My Agents:
![agents](https://github.com/user-attachments/assets/c556b8b4-917f-4df1-bec3-eeb06e6f9638)


My slack workspace (Naik Corporation)
![slack_dem](https://github.com/user-attachments/assets/27722ece-6462-4018-9b22-c9e1fc58fdb7)

