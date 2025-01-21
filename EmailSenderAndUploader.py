import os
from time import sleep as wait, sleep
import json
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from PIL import Image
import cv2
import fitz  # PyMuPDF
import numpy as np  # Import numpy for OpenCV compatibility
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
EMAILS_FILE = "../../../EmailsFile"
UPLOADED_VIDEO_FILE = "uploaded_video.json"  # To track uploaded videos

def get_current_day():
    # Get the current day of the week (e.g., Mon, Tue, Wed)
    current_day = datetime.now().strftime('%a')
    return current_day

def authenticate():
    credentials = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
            credentials = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(credentials, token)
    return credentials


def upload_video(file_path, title, description, category_id="22", tags=None):
    credentials = authenticate()
    youtube = build("youtube", "v3", credentials=credentials)

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or [],
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": "public"
        }
    }

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    print("Upload complete!")
    print("Video ID:", response["id"])
    return f"https://www.youtube.com/watch?v={response['id']}"


def get_video_description(today_day, emails):
    num_people = len(emails.get(today_day, []))
    return (f"YoutubeDescription")


def load_emails():
    try:
        with open(EMAILS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_uploaded_video(video_link, today_date):
    try:
        data = {}
        if os.path.exists(UPLOADED_VIDEO_FILE):
            with open(UPLOADED_VIDEO_FILE, "r") as file:
                data = json.load(file)
        data[today_date] = video_link
        with open(UPLOADED_VIDEO_FILE, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error saving uploaded video data: {e}")


def load_uploaded_video(today_date):
    try:
        if os.path.exists(UPLOADED_VIDEO_FILE):
            with open(UPLOADED_VIDEO_FILE, "r") as file:
                data = json.load(file)
                return data.get(today_date)
    except Exception as e:
        print(f"Error loading uploaded video data: {e}")
    return None

# Ensure send_email is defined above manage_emails
def send_email(to_email, today_date, video_link):
    from_email = "YourEmail"
    subject = f"Subject"
    message = ("Message")

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    attachment_path = f"Attachment File"
    if os.path.exists(attachment_path):
        try:
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename={os.path.basename(attachment_path)}")
                msg.attach(part)
        except Exception as e:
            print(f"Error attaching file: {e}")
    else:
        print(f"File '{attachment_path}' not found. No attachment will be sent.")

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, "ChromeAppPassword")
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print(f"Email has been sent to {to_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

def print_emails():
    emails = load_emails()

    print("\nCurrent email list by day:")
    for day, email_list in emails.items():
        print(f"{day.capitalize()}:")
        sleep(1)
        if email_list:
            for idx, email in enumerate(email_list, 1):
                print(f"  {idx}. {email}")

        else:
            print("  No emails for this day.")
    sleep(1)

def manage_emails():
    emails = load_emails()

    while True:


        action = input("\nChoose an action: \n1. Add email\n2. Delete email\n3. Send emails to all\n4. Send an email to an individual\n5. Show emails list\n6. Quit\nEnter your choice: ")

        if action == "1":
            new_email = input("Enter the email to add: ").strip()
            day = input("Enter the day for the email (Mon, Tue, etc.): ").strip().lower()
            if day not in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]:
                print("Invalid day. Please enter a valid weekday abbreviation (Mon, Tue, etc.).")
                continue
            if day not in emails:
                emails[day] = []
            if new_email not in emails[day]:
                emails[day].append(new_email)
                print(f"Added {new_email} to {day}.")
            else:
                print(f"{new_email} is already in the list for {day}.")
            with open(EMAILS_FILE, "w") as file:
                json.dump(emails, file, indent=4)

        elif action == "2":
            email_to_delete = input("Enter the email to delete: ").strip()
            day = input("Enter the day for the email (Mon, Tue, etc.): ").strip().lower()
            if day in emails and email_to_delete in emails[day]:
                emails[day].remove(email_to_delete)
                print(f"Deleted {email_to_delete} from {day}.")
                with open(EMAILS_FILE, "w") as file:
                    json.dump(emails, file, indent=4)
            else:
                print(f"{email_to_delete} was not found for {day}.")

        elif action == "3":
            today_date = datetime.today().strftime('%Y-%m-%d')
            today_day = datetime.today().strftime('%a').lower()
            video_link = load_uploaded_video(today_date)

            if not video_link:
                pdf_file = f"PathToPDFFile"
                if not os.path.exists(pdf_file):
                    print(f"PDF file for today ({today_date}) not found. Please generate it first.")
                    continue

                # Convert PDF to images
                doc = fitz.open(pdf_file)
                images = [Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                          for pix in (page.get_pixmap() for page in doc)]

                # Create video
                video_file = f"daily_comics_{today_date}.mp4"
                width, height = images[0].size
                out = cv2.VideoWriter(video_file, cv2.VideoWriter_fourcc(*'mp4v'), 0.2, (width, height))
                for img in images:
                    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                    out.write(img_cv)
                out.release()

                # Upload video
                video_title = f"Daily Comics for {today_date}"
                video_description = get_video_description(today_day, emails)
                video_link = upload_video(video_file, video_title, video_description)
                save_uploaded_video(video_link, today_date)

            if today_day in emails:
                for email in emails[today_day]:
                    send_email(email, today_date, video_link)

        elif action == "4":
            recipient = input("Enter the recipient's email or type 'test' to send to you: ").strip()
            if recipient.lower() == "test":
                recipient = "YourEmailForQuickAccess"

            today_date = datetime.today().strftime('%Y-%m-%d')
            video_link = load_uploaded_video(today_date)

            if not video_link:
                pdf_file = f"PathToPDFFile"
                if not os.path.exists(pdf_file):
                    print(f"PDF file for today ({today_date}) not found. Please generate it first.")
                    continue

                # Convert PDF to images
                doc = fitz.open(pdf_file)
                images = [Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                          for pix in (page.get_pixmap() for page in doc)]

                # Create video
                video_file = f"daily_comics_{today_date}.mp4"
                width, height = images[0].size
                out = cv2.VideoWriter(video_file, cv2.VideoWriter_fourcc(*'mp4v'), 0.2, (width, height))
                for img in images:
                    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                    out.write(img_cv)
                out.release()

                current_day = get_current_day()
                if current_day == "Sun":
                    video_title = f"{today_date}'s Sunday Comics!!"  # Sunday Comics (hash out manually)
                else:
                    video_title = f"Daily Comics for {today_date}"  # Daily comics (hash out manually)

                # Upload video
                video_description = get_video_description(datetime.today().strftime('%a').lower(), emails)
                video_link = upload_video(video_file, video_title, video_description)
                save_uploaded_video(video_link, today_date)

            send_email(recipient, today_date, video_link)

        elif action == "5":
            print_emails()

        elif action == "6":
            print("Exiting program.")
            quit()

        else:
            print("Invalid choice. Please select 1, 2, 3, 4, or 5.")



if __name__ == "__main__":
    manage_emails()
