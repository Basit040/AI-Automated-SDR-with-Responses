#!/usr/bin/env python3
"""
Simple Free AI SDR System with Email Reply Handling
===================================================

A completely free AI Sales Development Representative system that:
1. Generates cold emails using multiple AI personas
2. Sends emails via free SMTP (Gmail/Outlook)  
3. Handles email replies via webhook callbacks
4. Continues conversations automatically

Free Services Used:
- OpenAI API (free tier available)
- Gmail/Outlook SMTP (free)
- ngrok for webhook tunneling (free tier)
- Local webhook server (built-in)

Usage:
    uv run simple_sdr.py

Requirements:
    - OpenAI API key
    - Gmail/Outlook email account
    - App password for email account
"""

import os
import asyncio
import json
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, List
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from threading import Thread
import time

# Import OpenAI for direct API calls (simpler than agents framework)
import openai


class SimpleSDR:
    """
    Simple SDR system using free services for email outreach and reply handling.
    """
    
    def __init__(self):
        """Initialize with free email service configuration."""
        print("🤖 Initializing Simple Free AI SDR System...")
        
        load_dotenv(override=True)
        
        # Verify OpenAI API key
        if not os.environ.get('OPENAI_API_KEY'):
            raise ValueError("❌ OPENAI_API_KEY required - get free tier at https://platform.openai.com")
        
        openai.api_key = os.environ.get('OPENAI_API_KEY')
        
        # Email configuration - UPDATE THESE
        self.email_address = os.environ.get('EMAIL_ADDRESS', 'your-email@gmail.com')
        self.email_password = os.environ.get('EMAIL_PASSWORD', 'your-app-password')
        self.smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        self.imap_server = os.environ.get('IMAP_SERVER', 'imap.gmail.com')
        
        # Company info
        self.company_name = "ComplAI"
        self.company_description = "AI-powered SOC2 compliance automation"
        
        # Conversation memory
        self.conversations = {}
        
        print("✅ Simple SDR initialized successfully")
    
    def generate_cold_email(self, persona: str, recipient: str = "CEO") -> str:
        """
        Generate a cold email using OpenAI with different personas.
        
        Args:
            persona: "professional", "engaging", or "concise"
            recipient: Target recipient title
            
        Returns:
            Generated email content
        """
        personas = {
            "professional": "Write a professional, formal cold sales email",
            "engaging": "Write a witty, engaging cold sales email that's likely to get a response", 
            "concise": "Write a brief, direct cold sales email that gets straight to the point"
        }
        
        prompt = f"""
        {personas.get(persona, personas["professional"])}.
        
        Company: {self.company_name}
        Product: {self.company_description}
        Recipient: {recipient}
        
        Make it compelling and personalized. Include a clear call to action.
        Keep it under 150 words.
        """
        
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",  # Cheaper than gpt-4
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"❌ Error generating email: {e}")
            return f"Hi {recipient},\n\nI'd love to show you how {self.company_name} can help with {self.company_description}.\n\nInterested in a quick chat?\n\nBest regards"
    
    def select_best_email(self, emails: List[str]) -> str:
        """
        Use AI to select the best email from generated options.
        
        Args:
            emails: List of email content options
            
        Returns:
            Selected best email
        """
        prompt = f"""
        Pick the best cold sales email from these options. Consider which one a busy executive would be most likely to respond to.
        
        Return only the selected email, no explanation.
        
        Options:
        
        1. {emails[0]}
        
        2. {emails[1]}
        
        3. {emails[2]}
        """
        
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"❌ Error selecting email: {e}")
            return emails[0]  # Fallback to first email
    
    def send_email_smtp(self, to_email: str, subject: str, body: str) -> bool:
        """
        Send email using free SMTP service (Gmail/Outlook).
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body content
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add reply-to header for webhook handling
            msg['Reply-To'] = self.email_address
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send via SMTP
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_address, self.email_password)
            text = msg.as_string()
            server.sendmail(self.email_address, to_email, text)
            server.quit()
            
            print(f"✅ Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            print("💡 Common issues:")
            print("   • Enable 2FA and use App Password for Gmail")
            print("   • Check SMTP settings for your email provider")
            print("   • Verify email/password in .env file")
            return False
    
    def generate_reply(self, original_email: str, reply_content: str) -> str:
        """
        Generate an AI reply to continue the conversation.
        
        Args:
            original_email: The original cold email sent
            reply_content: The prospect's reply content
            
        Returns:
            Generated reply email
        """
        prompt = f"""
        You are a sales representative for {self.company_name}, which provides {self.company_description}.
        
        A prospect replied to your cold email. Generate a helpful, professional response that continues the conversation.
        
        Original email you sent:
        {original_email}
        
        Their reply:
        {reply_content}
        
        Write a response that:
        1. Acknowledges their reply
        2. Provides helpful information
        3. Moves the conversation forward
        4. Includes a clear next step
        
        Keep it conversational and under 200 words.
        """
        
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"❌ Error generating reply: {e}")
            return "Thank you for your reply! I'd love to continue our conversation. When would be a good time for a brief call?"
    
    def check_for_replies(self):
        """
        Check email inbox for replies using IMAP (free).
        This runs as a background process.
        """
        try:
            # Connect to IMAP server
            mail = imaplib.IMAP4_SSL(self.imap_server)
            mail.login(self.email_address, self.email_password)
            mail.select('inbox')
            
            # Search for unread emails
            status, messages = mail.search(None, 'UNSEEN')
            
            if status == 'OK':
                for msg_id in messages[0].split():
                    # Fetch email
                    status, msg_data = mail.fetch(msg_id, '(RFC822)')
                    
                    if status == 'OK':
                        email_body = msg_data[0][1]
                        email_message = email.message_from_bytes(email_body)
                        
                        from_email = email_message['From']
                        subject = email_message['Subject']
                        
                        # Get email content
                        body = ""
                        if email_message.is_multipart():
                            for part in email_message.walk():
                                if part.get_content_type() == "text/plain":
                                    body = part.get_payload(decode=True).decode()
                                    break
                        else:
                            body = email_message.get_payload(decode=True).decode()
                        
                        print(f"📧 New reply from {from_email}: {subject}")
                        
                        # Process the reply
                        self.handle_reply(from_email, subject, body)
                        
                        # Mark as read
                        mail.store(msg_id, '+FLAGS', '\\Seen')
            
            mail.close()
            mail.logout()
            
        except Exception as e:
            print(f"❌ Error checking replies: {e}")
    
    def handle_reply(self, from_email: str, subject: str, body: str):
        """
        Handle incoming email reply by generating and sending AI response.
        
        Args:
            from_email: Sender's email address
            subject: Email subject
            body: Reply content
        """
        print(f"🤖 Processing reply from {from_email}")
        
        # Get conversation history
        conversation_key = from_email.lower()
        original_email = self.conversations.get(conversation_key, "")
        
        # Generate AI reply
        reply = self.generate_reply(original_email, body)
        
        # Send reply
        reply_subject = f"Re: {subject}" if not subject.startswith('Re:') else subject
        success = self.send_email_smtp(from_email, reply_subject, reply)
        
        if success:
            # Update conversation history
            self.conversations[conversation_key] = f"{original_email}\n\n--- THEIR REPLY ---\n{body}\n\n--- MY REPLY ---\n{reply}"
            print(f"✅ Auto-reply sent to {from_email}")
        else:
            print(f"❌ Failed to send auto-reply to {from_email}")
    
    async def run_cold_email_campaign(self, recipients: List[str]):
        """
        Run a complete cold email campaign.
        
        Args:
            recipients: List of email addresses to send to
        """
        print("🚀 Starting Cold Email Campaign...")
        print("=" * 50)
        
        for recipient in recipients:
            print(f"\n📧 Processing recipient: {recipient}")
            
            # Step 1: Generate multiple email options
            print("   🎭 Generating emails with different personas...")
            emails = []
            personas = ["professional", "engaging", "concise"]
            
            for persona in personas:
                email_content = self.generate_cold_email(persona)
                emails.append(email_content)
                print(f"      ✅ {persona.title()} email generated")
            
            # Step 2: Select best email
            print("   🎯 Selecting best email...")
            best_email = self.select_best_email(emails)
            
            # Step 3: Generate subject line
            subject_prompt = f"Write a compelling email subject line for this cold sales email:\n\n{best_email}\n\nMake it likely to get opened. Under 50 characters."
            
            try:
                subject_response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": subject_prompt}],
                    max_tokens=50,
                    temperature=0.7
                )
                subject = subject_response.choices[0].message.content.strip().replace('"', '')
            except:
                subject = f"Quick question about {self.company_name}"
            
            print(f"   📝 Subject: {subject}")
            
            # Step 4: Send email
            print("   📤 Sending email...")
            success = self.send_email_smtp(recipient, subject, best_email)
            
            if success:
                # Store conversation for reply handling
                self.conversations[recipient.lower()] = best_email
                print(f"   ✅ Campaign email sent to {recipient}")
            else:
                print(f"   ❌ Failed to send to {recipient}")
            
            # Add delay between emails to avoid spam detection
            print("   ⏱️  Waiting 30 seconds before next email...")
            await asyncio.sleep(30)
        
        print("\n🎊 Cold email campaign completed!")
        print("📬 Monitoring for replies... (Press Ctrl+C to stop)")
    
    def start_reply_monitoring(self):
        """Start monitoring for email replies in background."""
        def monitor():
            while True:
                try:
                    self.check_for_replies()
                    time.sleep(60)  # Check every minute
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"❌ Reply monitoring error: {e}")
                    time.sleep(60)
        
        # Start monitoring in background thread
        monitor_thread = Thread(target=monitor, daemon=True)
        monitor_thread.start()
        return monitor_thread


# Webhook server for advanced reply handling (alternative to IMAP polling)
app = Flask(__name__)

@app.route('/webhook/email-reply', methods=['POST'])
def handle_webhook_reply():
    """
    Handle email replies via webhook (for advanced setup).
    This can be used instead of IMAP polling for real-time replies.
    """
    try:
        data = request.json
        
        # Extract email data (format depends on your email service webhook)
        from_email = data.get('from')
        subject = data.get('subject')
        body = data.get('body')
        
        print(f"📨 Webhook reply from {from_email}: {subject}")
        
        # Initialize SDR and handle reply
        sdr = SimpleSDR()
        sdr.handle_reply(from_email, subject, body)
        
        return jsonify({"status": "success", "message": "Reply processed"})
        
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


def run_webhook_server():
    """Run the webhook server for handling email replies."""
    print("🌐 Starting webhook server on http://localhost:5000")
    print("💡 Use ngrok to expose this publicly: ngrok http 5000")
    app.run(host='0.0.0.0', port=5000, debug=False)


async def main():
    """Main function to run the Simple SDR system."""
    print("🎉 Welcome to Simple Free AI SDR System!")
    print("=" * 60)
    print("Free Services Used:")
    print("• OpenAI API (free tier available)")
    print("• Gmail/Outlook SMTP (free)")
    print("• Local IMAP monitoring (free)")
    print("• Built-in webhook server (free)")
    print("=" * 60)
    
    try:
        # Initialize SDR
        sdr = SimpleSDR()
        
        # Configuration check
        if sdr.email_address == 'your-email@gmail.com':
            print("❌ Please update your email configuration!")
            print("1. Update EMAIL_ADDRESS in .env or script")
            print("2. Set EMAIL_PASSWORD (use App Password for Gmail)")
            print("3. Update SMTP/IMAP servers if not using Gmail")
            return
        
        # Test email sending
        print("\n📤 Testing email configuration...")
        test_success = sdr.send_email_smtp(
            sdr.email_address,  # Send test to yourself
            "Test - Simple SDR System",
            "This is a test email from your Simple SDR system. If you receive this, email sending is working!"
        )
        
        if not test_success:
            print("❌ Email test failed. Please check your configuration.")
            return
        
        print("✅ Email test successful!")
        
        # Demo: Generate sample emails
        print("\n🎭 Demo: Generating sample emails...")
        sample_emails = []
        for persona in ["professional", "engaging", "concise"]:
            email = sdr.generate_cold_email(persona, "Startup CEO")
            sample_emails.append(email)
            print(f"\n--- {persona.upper()} EMAIL ---")
            print(email[:200] + "..." if len(email) > 200 else email)
        
        # Demo: Select best email
        print(f"\n🎯 Demo: AI selecting best email...")
        best = sdr.select_best_email(sample_emails)
        print("--- SELECTED BEST EMAIL ---")
        print(best)
        
        # Ask user for campaign
        print("\n" + "="*60)
        print("READY FOR LIVE CAMPAIGN")
        print("="*60)
        
        # Example recipients (replace with real emails)
        example_recipients = [
            "abdulbasitnedian@outlook.com.com",
            "abdulbasitnedian@gmail.com"
        ]
        
        print("Example usage:")
        print("1. Update recipient list in the script")
        print("2. Run campaign: await sdr.run_cold_email_campaign(recipients)")
        print("3. Monitor replies automatically")
        
        # Uncomment to run actual campaign:
        # await sdr.run_cold_email_campaign(example_recipients)
        
        # Start reply monitoring
        print("\n📬 Starting reply monitoring...")
        sdr.start_reply_monitoring()
        
        # Keep running
        print("🔄 System running... Press Ctrl+C to stop")
        while True:
            await asyncio.sleep(10)
    
    except KeyboardInterrupt:
        print("\n👋 Simple SDR system stopped by user")
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\n🔧 Setup Instructions:")
        print("1. Get free OpenAI API key: https://platform.openai.com")
        print("2. Create .env file with EMAIL_ADDRESS and EMAIL_PASSWORD")
        print("3. Enable App Password for Gmail (if using Gmail)")
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")


if __name__ == "__main__":
    # Choose mode: SDR system or webhook server
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "webhook":
        # Run webhook server
        run_webhook_server()
    else:
        # Run main SDR system
        asyncio.run(main())
