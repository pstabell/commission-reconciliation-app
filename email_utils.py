"""Email utilities for the Agent Commission Tracker app."""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logger = logging.getLogger(__name__)

def send_email(to_email: str, subject: str, html_body: str, text_body: str = None):
    """Send an email using SMTP.
    
    For production, you'll want to use a service like:
    - SendGrid
    - AWS SES
    - Postmark
    - Mailgun
    
    For MVP, this uses SMTP with environment variables.
    """
    
    # Get email configuration from environment
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    from_email = os.getenv("FROM_EMAIL", smtp_user)
    
    if not smtp_user or not smtp_pass:
        logger.error("Email configuration missing. Set SMTP_USER and SMTP_PASS environment variables.")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"Agent Commission Tracker <{from_email}>"
        msg['To'] = to_email
        
        # Add text and HTML parts
        if text_body:
            msg.attach(MIMEText(text_body, 'plain'))
        msg.attach(MIMEText(html_body, 'html'))
        
        # Send email
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
            
        logger.info(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False

def send_password_reset_email(to_email: str, reset_link: str):
    """Send password reset email."""
    
    subject = "Reset Your Agent Commission Tracker Password"
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
            .content {{ background-color: #f9f9f9; padding: 30px; }}
            .button {{ display: inline-block; padding: 12px 30px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 30px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Agent Commission Tracker</h1>
            </div>
            <div class="content">
                <h2>Password Reset Request</h2>
                <p>Hi there,</p>
                <p>We received a request to reset your password. Click the button below to create a new password:</p>
                <p style="text-align: center;">
                    <a href="{reset_link}" class="button">Reset Password</a>
                </p>
                <p>This link will expire in 1 hour for security reasons.</p>
                <p>If you didn't request a password reset, please ignore this email.</p>
                <p><strong>Direct link:</strong><br>
                <a href="{reset_link}">{reset_link}</a></p>
            </div>
            <div class="footer">
                <p>© 2024 Metro Technology Solutions LLC. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_body = f"""
    Agent Commission Tracker - Password Reset Request
    
    Hi there,
    
    We received a request to reset your password. Visit the link below to create a new password:
    
    {reset_link}
    
    This link will expire in 1 hour for security reasons.
    
    If you didn't request a password reset, please ignore this email.
    
    © 2024 Metro Technology Solutions LLC. All rights reserved.
    """
    
    return send_email(to_email, subject, html_body, text_body)

def send_welcome_email(to_email: str):
    """Send welcome email after subscription."""
    
    subject = "Your 14-Day Free Trial Has Started - Agent Commission Tracker"
    app_url = os.getenv("RENDER_APP_URL", "https://commission-tracker-app.onrender.com")
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
            .content {{ background-color: #f9f9f9; padding: 30px; }}
            .button {{ display: inline-block; padding: 12px 30px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .feature {{ background-color: white; padding: 15px; margin: 10px 0; border-left: 4px solid #4CAF50; }}
            .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 30px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Welcome to Agent Commission Tracker! 🎉</h1>
            </div>
            <div class="content">
                <h2>Your 14-day free trial has started!</h2>
                <p>Welcome to Agent Commission Tracker! You have full access to all features for the next 14 days.</p>
                <p><strong>No charges until your trial ends.</strong> You can cancel anytime.</p>
                
                <p style="text-align: center;">
                    <a href="{app_url}" class="button">Login to Your Account</a>
                </p>
                
                <h3>Getting Started:</h3>
                <div class="feature">
                    <strong>1. Add Your First Policy</strong><br>
                    Navigate to "Add New Policy Transaction" to start tracking commissions.
                </div>
                <div class="feature">
                    <strong>2. Import Existing Data</strong><br>
                    Use the "Tools" page to bulk import your existing policies via CSV.
                </div>
                <div class="feature">
                    <strong>3. Set Up Reconciliation</strong><br>
                    Use the "Reconciliation" feature to match carrier statements automatically.
                </div>
                
                <h3>Need Help?</h3>
                <p>Visit the Help section in the app for detailed guides and troubleshooting.</p>
                
                <h3>Your Account:</h3>
                <p>
                    <strong>Email:</strong> {to_email}<br>
                    <strong>Plan:</strong> Professional (Free for 14 days, then $19.99/month)<br>
                    <strong>Trial Ends:</strong> 14 days from today<br>
                    <strong>Billing:</strong> Your card will be charged after the trial unless you cancel
                </p>
            </div>
            <div class="footer">
                <p>© 2024 Metro Technology Solutions LLC. All rights reserved.</p>
                <p>You're receiving this because you signed up for Agent Commission Tracker.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_body = f"""
    Welcome to Agent Commission Tracker! 🎉
    
    Your 14-day free trial has started!
    
    Welcome to Agent Commission Tracker! You have full access to all features for the next 14 days.
    
    No charges until your trial ends. You can cancel anytime.
    
    Login here: {app_url}
    
    Getting Started:
    1. Add Your First Policy - Navigate to "Add New Policy Transaction" to start tracking commissions.
    2. Import Existing Data - Use the "Tools" page to bulk import your existing policies via CSV.
    3. Set Up Reconciliation - Use the "Reconciliation" feature to match carrier statements automatically.
    
    Need Help?
    Visit the Help section in the app for detailed guides and troubleshooting.
    
    Your Account:
    Email: {to_email}
    Plan: Professional (Free for 14 days, then $19.99/month)
    Trial Ends: 14 days from today
    Billing: Your card will be charged after the trial unless you cancel
    
    © 2024 Metro Technology Solutions LLC. All rights reserved.
    """
    
    return send_email(to_email, subject, html_body, text_body)