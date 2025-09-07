# 🤖 Simple Free AI SDR System

A completely **FREE** AI Sales Development Representative system that automatically generates cold emails, sends them, and handles replies to continue conversations. No paid services required beyond OpenAI API!

## 🎯 What It Does

1. **Generates Cold Emails** - 3 AI personas create different email styles
2. **Selects Best Email** - AI picks the most effective email automatically  
3. **Sends Emails** - Uses free SMTP (Gmail/Outlook) to send emails
4. **Handles Replies** - Automatically responds to prospect replies with AI
5. **Continues Conversations** - Keeps conversation history and context

## 🆓 100% Free Services Used

- **OpenAI API** - Free tier available (enough for testing)
- **Gmail/Outlook SMTP** - Free email sending
- **IMAP Email Monitoring** - Free reply detection
- **Built-in Webhook Server** - Free local server for advanced features
- **No SendGrid Required** - Uses your existing email account

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8+
- Gmail or Outlook email account
- OpenAI API key (free tier: https://platform.openai.com)

### 2. Setup

```bash
# Clone/download the files
# Install dependencies
uv add openai python-dotenv flask

# Create .env file
touch .env
```

### 3. Configure Environment

Create `.env` file:

```env
# OpenAI API Key (required)
OPENAI_API_KEY=your_openai_api_key_here

# Email Configuration (Gmail example)
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password-here
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
IMAP_SERVER=imap.gmail.com
```

### 4. Gmail Setup (Most Common)

1. **Enable 2-Factor Authentication** in Gmail
2. **Generate App Password**:
   - Go to Google Account settings
   - Security → App passwords
   - Generate password for "Mail"
   - Use this as `EMAIL_PASSWORD` in .env

### 5. Run the System

```bash
# Test the system
uv run simple_sdr.py

# Or run webhook server (advanced)
uv run simple_sdr.py webhook
```

## 📋 Features

### **AI Email Generation**
```python
# Generates 3 different styles automatically:
- Professional: Formal, serious tone
- Engaging: Witty, conversational tone  
- Concise: Brief, direct approach
```

### **Smart Email Selection**
- AI automatically picks the most effective email
- Considers recipient psychology and response likelihood

### **Free Email Sending**
- Uses your existing Gmail/Outlook account
- No additional email service costs
- Built-in SMTP configuration

### **Automatic Reply Handling**
- Monitors inbox for replies every minute
- Generates contextual AI responses
- Maintains conversation history
- Continues nurturing prospects automatically

### **Webhook Support**
- Alternative to IMAP polling
- Real-time reply processing
- Can integrate with email services that support webhooks

## 🔧 Configuration Options

### **Email Providers**

**Gmail:**
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
IMAP_SERVER=imap.gmail.com
```

**Outlook/Hotmail:**
```env
SMTP_SERVER=smtp-mail.outlook.com  
SMTP_PORT=587
IMAP_SERVER=outlook.office365.com
```

**Yahoo:**
```env
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
IMAP_SERVER=imap.mail.yahoo.com
```

### **Company Customization**

Edit in `simple_sdr.py`:
```python
self.company_name = "YourCompany"
self.company_description = "Your product description"
```

## 📧 Running Email Campaigns

### **Basic Usage:**

```python
# 1. Update recipient list in simple_sdr.py
recipients = [
    "prospect1@company.com",
    "prospect2@startup.com", 
    "ceo@techcompany.com"
]

# 2. Run campaign (uncomment in main())
await sdr.run_cold_email_campaign(recipients)
```

### **What Happens:**
1. **Generate 3 emails** for each recipient (different AI personas)
2. **Select best email** using AI evaluation
3. **Create compelling subject line** using AI
4. **Send email** via SMTP
5. **Wait 30 seconds** between emails (avoid spam)
6. **Monitor for replies** and respond automatically

## 🔄 Reply Handling Process

When someone replies to your cold email:

1. **Detection**: System checks inbox every 60 seconds
2. **Processing**: Extracts reply content and sender info
3. **Context**: Retrieves original email conversation
4. **AI Response**: Generates contextual reply using OpenAI
5. **Send Reply**: Automatically sends response via SMTP
6. **History**: Updates conversation history for future context

## 🛠️ Advanced Features

### **Webhook Server**

For real-time reply handling instead of polling:

```bash
# Start webhook server
uv run simple_sdr.py webhook

# Expose publicly with ngrok (free)
ngrok http 5000
```

### **Conversation Memory**

The system remembers entire conversation threads:
- Original cold email sent
- All prospect replies
- All AI responses sent
- Uses context for better follow-up responses

### **Campaign Analytics**

Monitor in console output:
- Emails sent successfully
- Failed sends with error details
- Replies received and processed
- Auto-responses sent

## 🔍 Troubleshooting

### **Email Not Sending**

```
❌ Error: Authentication failed
```
**Solution**: Use App Password, not regular password for Gmail

```
❌ Error: SMTP connection failed  
```
**Solution**: Check SMTP server settings for your email provider

### **No Replies Detected**

```
❌ Error: IMAP login failed
```
**Solution**: Enable IMAP in email settings (Gmail: Settings → Forwarding/POP-IMAP)

### **OpenAI API Errors**

```
❌ Error: Rate limit exceeded
```
**Solution**: You've hit free tier limits. Wait or upgrade OpenAI plan.

## 💡 Pro Tips

### **Avoid Spam Filters**
- Use your real email address (builds trust)
- Don't send too many emails at once (30-second delays built-in)
- Personalize emails for each recipient
- Monitor reply rates and adjust approach

### **Improve Response Rates**
- Test different personas and track which works best
- A/B test subject lines
- Follow up on conversations promptly (automatic with this system)
- Keep initial emails under 150 words

### **Scale Responsibly**
- Start with small batches (5-10 emails)
- Monitor spam folder placement
- Adjust sending frequency based on provider limits
- Keep conversation quality high with AI responses

## 🔒 Security & Privacy

- **API Keys**: Never commit .env files to git
- **Email Passwords**: Use App Passwords, not main password
- **Conversation Data**: Stored locally in memory only
- **No External Services**: All data stays on your machine

## 📊 Cost Breakdown

- **OpenAI API**: ~$0.01 per email (free tier covers testing)
- **Email Sending**: $0 (uses your email account)
- **Server Hosting**: $0 (runs locally)
- **Webhook Tunneling**: $0 (ngrok free tier)

**Total Monthly Cost**: Under $10 even for hundreds of emails!

## 🚀 Getting Started Checklist

- [ ] Get OpenAI API key (free tier)
- [ ] Setup Gmail App Password
- [ ] Create .env file with credentials  
- [ ] Run test: `uv run simple_sdr.py`
- [ ] Verify test email received
- [ ] Update company info in script
- [ ] Add real prospect email addresses
- [ ] Uncomment campaign code and run
- [ ] Monitor console for replies and auto-responses

## 🤝 Support

**Common Issues:**
- Gmail setup problems → Check App Password setup
- SMTP errors → Verify email provider settings  
- No replies detected → Enable IMAP in email settings
- OpenAI errors → Check API key and usage limits

**Need Help?**
- Check console output for detailed error messages
- Test email sending with yourself first
- Start with 1-2 test emails before bulk campaigns

---

**Ready to automate your sales outreach for FREE!** 🎉

Run `uv run simple_sdr.py` and watch the AI generate, send, and handle email conversations automatically.
