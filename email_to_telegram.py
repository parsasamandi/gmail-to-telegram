# ALGORITHM OVERVIEW
# ================
# This program forwards unread Gmail emails to Telegram.
# Here's how it works step by step:
#
# 1. SETUP PHASE:
#    - Load secret information (API keys) from environment variables or .env file
#    - Set up Gmail API permissions (scopes) for reading/modifying emails
#    - Configure Telegram bot token and chat ID
#
# 2. INITIALIZATION:
#    - Create an EmailToTelegram object
#    - Authenticate with Gmail API (login process if needed)
#
# 3. RUNNING MODES:
#    - ONE-TIME MODE (--once flag):
#      * Check for unread emails once
#      * Process them and exit
#    - CONTINUOUS MODE (default):
#      * Keep checking for new emails every few minutes
#      * Run until user stops with Ctrl+C
#
# 4. EMAIL CHECKING PROCESS:
#    - Connect to Gmail and search for unread emails
#    - For each unread email found:
#      a. Get the full email details (subject, sender, date, body)
#      b. Format the email info into a nice message
#      c. Send the message to Telegram
#      d. If sending succeeded, mark the email as read in Gmail
#      e. Wait 1 second before processing next email
#
# 5. CONTINUOUS LOOP (if in continuous mode):
#    - After checking emails, sleep for the specified interval
#    - Repeat the email checking process
#    - Continue until interrupted
#
# TECHNICAL DETAILS:
# - Uses Gmail API to access emails securely
# - Stores login credentials in token.json to avoid re-login
# - Sends formatted messages to Telegram using their API
# - Handles errors gracefully and continues running
# - Limits message length to fit Telegram's limits

# These are the tools (libraries) we need for our program
import os  # For working with files and the operating system
import base64  # For decoding email content that's encoded
import time  # For waiting/sleeping between checks
from datetime import datetime  # For getting current date and time
from google.auth.transport.requests import Request  # For refreshing Google credentials
from google.oauth2.credentials import Credentials  # For storing Google login info
from google_auth_oauthlib.flow import InstalledAppFlow  # For the Google login process
from googleapiclient.discovery import build  # For connecting to Google APIs
import requests  # For sending messages to Telegram
from dotenv import load_dotenv  # For loading secret info from .env file

# Load secret information from a .env file (like passwords, but for API keys)
load_dotenv()

# This tells Google what permissions we need (we want to read and modify emails)
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# These are the settings for Telegram
# TELEGRAM_BOT_TOKEN is like a password for our bot to send messages
# os.getenv gets the value from environment variables or .env file, or uses the default
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
# TELEGRAM_CHAT_ID is the ID of the chat where we send messages (your saved messages)
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', 'YOUR_CHAT_ID_HERE')

# This is a class - a blueprint for creating objects
# EmailToTelegram is our main class that handles checking Gmail and sending to Telegram
class EmailToTelegram:
    def __init__(self):
        # This is the __init__ method, also called the constructor.
        # It runs automatically when we create a new object from this class.
        # 'self' is a special word that refers to the object we're creating.
        # It's like saying "this object" in the code.
        
        # We set gmail_service to None at first because we haven't connected to Gmail yet.
        # Later, we'll put the Gmail connection here.
        self.gmail_service = None
        
        # This is the name of a file where we might save when we last checked for emails.
        # We don't use it in this code, but it's here for future use.
        self.last_check_file = 'last_check.txt'
        
    def authenticate_gmail(self):
        """Authenticate with Gmail API"""
        # This function connects our program to Gmail so we can read emails.
        # It uses Google's security system to make sure we're allowed to access the emails.
        
        # Start with no credentials (creds is short for credentials)
        creds = None
        
        # Check if we already have saved login info from a previous run
        # os.path.exists checks if the file 'token.json' exists on the computer
        if os.path.exists('token.json'):
            # If the file exists, load the saved credentials from it
            # Credentials.from_authorized_user_file reads the file and creates a credentials object
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        # Now check if we have valid credentials
        # If creds is None (no file) or not valid (expired or wrong), we need new ones
        if not creds or not creds.valid:
            # If we have expired credentials but can refresh them (get new ones without logging in again)
            if creds and creds.expired and creds.refresh_token:
                # Refresh the credentials using the refresh token
                creds.refresh(Request())
            else:
                # We need to do a full login process
                # InstalledAppFlow.from_client_secrets_file sets up the login flow using our app's secret info
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                # run_local_server starts a web server on your computer for the login
                creds = flow.run_local_server(port=0)
            
            # Save the new credentials to token.json for next time
            # 'with open' opens the file for writing
            with open('token.json', 'w') as token:
                # creds.to_json() converts the credentials to a text format (JSON)
                token.write(creds.to_json())
        
        # Now that we have valid credentials, create the Gmail service
        # build() creates a connection to Gmail's API using our credentials
        self.gmail_service = build('gmail', 'v1', credentials=creds)
        # Print a success message
        print("✓ Gmail authenticated successfully")
    
    def get_unread_emails(self):
        """Fetch unread emails from Gmail"""
        # This function gets a list of unread emails from Gmail.
        # It asks Gmail for emails that haven't been read yet.
        
        try:
            # We use a try-except block in case something goes wrong
            
            # Search for unread messages using Gmail's search
            # self.gmail_service.users().messages().list() is the Gmail API call
            # userId='me' means the current user (you)
            # q='is:unread' is the search query for unread emails
            # maxResults=10 means get at most 10 emails
            results = self.gmail_service.users().messages().list(
                userId='me',
                q='is:unread',
                maxResults=5
            ).execute()
            
            # The results come back as a dictionary
            # .get('messages', []) gets the list of messages, or empty list if none
            messages = results.get('messages', [])
            # Return the list of messages (each is a dict with 'id')
            return messages
        except Exception as e:
            # If there's an error, print it and return empty list
            print(f"Error fetching emails: {e}")
            return []
    
    def get_email_details(self, msg_id):
        """Get full details of an email"""
        # This function gets all the information about a specific email.
        # msg_id is the unique ID of the email we want details for.
        
        try:
            # Get the full message from Gmail
            # .get() fetches the complete email data
            # format='full' means get all parts of the email
            message = self.gmail_service.users().messages().get(
                userId='me',
                id=msg_id,
                format='full'
            ).execute()
            
            # The email headers contain info like subject, from, date
            # headers is a list of dictionaries with 'name' and 'value'
            headers = message['payload']['headers']
            
            # Find the subject header
            # next() gets the first item that matches the condition
            # (h['value'] for h in headers if h['name'] == 'Subject') creates a generator
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            
            # Find the sender
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            
            # Find the date
            date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')
            
            # Get the email body (the main content)
            body = self.get_email_body(message['payload'])
            
            # Return all the info in a dictionary
            return {
                'id': msg_id,
                'subject': subject,
                'sender': sender,
                'date': date,
                'body': body,
                'snippet': message.get('snippet', '')  # Short preview of the email
            }
        except Exception as e:
            # If error, print and return None
            print(f"Error getting email details: {e}")
            return None
    
    def get_email_body(self, payload):
        """Extract email body from payload"""
        # This function extracts the text content from an email.
        # Emails can have different formats, so we need to handle them carefully.
        # payload is the part of the email that contains the content.
        
        # Start with empty body
        body = ""
        
        # Check if the email has multiple parts (like text and HTML)
        if 'parts' in payload:
            # Loop through each part of the email
            for part in payload['parts']:
                # If this part is plain text
                if part['mimeType'] == 'text/plain':
                    # Check if there's actual data in this part
                    if 'data' in part['body']:
                        # The data is encoded in base64, so decode it
                        # base64.urlsafe_b64decode decodes the base64 string
                        # .decode('utf-8') converts bytes to text
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        # We found plain text, so stop looking
                        break
                # If this part is HTML and we haven't found text yet
                elif part['mimeType'] == 'text/html' and not body:
                    # Same decoding process for HTML
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
        else:
            # If no parts, the body might be directly in the payload
            if 'body' in payload and 'data' in payload['body']:
                body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        
        # Telegram has a limit of about 4096 characters per message
        # So we truncate long emails to 3500 chars + a note
        if len(body) > 3500:
            body = body[:3500] + "\n\n... (truncated)"
        
        # Return the extracted body text
        return body
    
    def send_to_telegram(self, email_data):
        """Send email content to Telegram Saved Messages"""
        # This function sends the email information to Telegram.
        # email_data is a dictionary with all the email details.
        
        try:
            # Format the message we want to send
            # Start with an emoji and "New Email"
            message = f"📧 *New Email*\n\n"
            # Add the sender
            message += f"*From:* {email_data['sender']}\n"
            # Add the subject
            message += f"*Subject:* {email_data['subject']}\n"
            # Add the date
            message += f"*Date:* {email_data['date']}\n"
            # Add a blank line
            message += f"\n*Content:*\n{email_data['snippet'][:500]}"
            # snippet is a short preview, limited to 500 chars
            
            # Create the URL for Telegram's API
            # f"..." is an f-string that puts variables into the string
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            
            # Prepare the data to send
            # This is what Telegram expects: chat_id, text, and parse_mode
            data = {
                'chat_id': TELEGRAM_CHAT_ID,  # Who to send to
                'text': message,              # The message content
                'parse_mode': 'Markdown'     # Use Markdown formatting (bold, etc.)
            }
            
            # Send the request to Telegram
            # requests.post sends data to a web server
            response = requests.post(url, json=data)
            
            # Check if it worked (HTTP status 200 means success)
            if response.status_code == 200:
                # Success! Print a message
                print(f"✓ Sent email to Telegram: {email_data['subject'][:50]}")
                return True
            else:
                # Failed, print the error
                print(f"✗ Failed to send to Telegram: {response.text}")
                return False
                
        except Exception as e:
            # If any error happened, print it
            print(f"Error sending to Telegram: {e}")
            return False
    
    def mark_as_read(self, msg_id):
        """Mark email as read"""
        # This function tells Gmail that we've read the email.
        # msg_id is the ID of the email to mark as read.
        
        try:
            # Use Gmail's API to modify the message
            # .modify() changes the email's labels
            # removeLabelIds: ['UNREAD'] removes the UNREAD label
            self.gmail_service.users().messages().modify(
                userId='me',
                id=msg_id,
                body={'removeLabelIds': ['UNREAD']}  # Remove the UNREAD label
            ).execute()
            # Print success message
            print(f"✓ Marked email as read: {msg_id}")
        except Exception as e:
            # If error, print it
            print(f"Error marking as read: {e}")
    
    def run_once(self):
        """Check for new emails once"""
        # This function checks for new emails one time.
        # It gets unread emails, sends them to Telegram, and marks them as read.
        
        # Print when we're starting the check
        print(f"\n🔍 Checking for new emails... [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
        
        # Get the list of unread emails
        unread_emails = self.get_unread_emails()
        
        # If no unread emails, tell the user
        if not unread_emails:
            print("No unread emails found")
            return
        
        # Tell how many we found
        print(f"Found {len(unread_emails)} unread email(s)")
        
        # Loop through each unread email
        for msg in unread_emails:
            # Get the full details of this email
            email_data = self.get_email_details(msg['id'])
            
            # If we got the details successfully
            if email_data:
                # Send it to Telegram
                if self.send_to_telegram(email_data):
                    # If sending worked, mark the email as read
                    self.mark_as_read(msg['id'])
                    # Wait 1 second between messages (be nice to the servers)
                    time.sleep(1)
    
    def run_continuous(self, interval_minutes=5):
        """Run continuously checking for new emails"""
        # This function runs forever, checking for emails every few minutes.
        # interval_minutes is how many minutes to wait between checks (default 5).
        
        # Tell the user we're starting
        print(f"🤖 Starting email monitor (checking every {interval_minutes} minutes)")
        print("Press Ctrl+C to stop\n")
        
        try:
            # Infinite loop - keeps running forever
            while True:
                # Check for emails once
                self.run_once()
                # Print that we're sleeping
                print(f"💤 Sleeping for {interval_minutes} minutes...")
                # Wait for the specified time
                # time.sleep() pauses the program
                # interval_minutes * 60 converts minutes to seconds
                time.sleep(interval_minutes * 60)
        except KeyboardInterrupt:
            # If the user presses Ctrl+C, this exception happens
            # Print a goodbye message
            print("\n\n👋 Stopping email monitor")

def main():
    # This is the main function that starts the program.
    # It's like the entry point - where the program begins running.
    
    # Create a new EmailToTelegram object
    bot = EmailToTelegram()
    
    # Connect to Gmail (authenticate)
    bot.authenticate_gmail()
    
    # Check how the user wants to run the program
    # sys.argv is a list of command line arguments
    # sys.argv[0] is the program name, [1] is the first argument
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        # If they passed '--once', run once and exit
        bot.run_once()
    else:
        # Otherwise, run continuously
        # If they passed a number, use it as interval, else default to 5
        interval = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 5
        bot.run_continuous(interval_minutes=interval)

if __name__ == '__main__':
    # This is a special Python thing
    # It means: only run main() if this file is run directly (not imported)
    main()
