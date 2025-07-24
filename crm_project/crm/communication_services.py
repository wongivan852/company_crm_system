# communication_services.py
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings
from django.core.mail import send_mail
from .models import CommunicationLog
import logging

logger = logging.getLogger(__name__)

class WhatsAppService:
    """
    WhatsApp Business API Integration
    Using Twilio WhatsApp API or Facebook WhatsApp Business API
    """
    
    def __init__(self):
        self.api_url = settings.WHATSAPP_API_URL
        self.access_token = settings.WHATSAPP_ACCESS_TOKEN
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
    
    def send_message(self, to_number, message, customer=None):
        """Send WhatsApp message"""
        try:
            # Format phone number (remove + and spaces)
            to_number = ''.join(filter(str.isdigit, to_number))
            
            payload = {
                "messaging_product": "whatsapp",
                "to": to_number,
                "type": "text",
                "text": {
                    "body": message
                }
            }
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                f"{self.api_url}/{self.phone_number_id}/messages",
                json=payload,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                message_id = result.get('messages', [{}])[0].get('id')
                
                # Log communication
                if customer:
                    CommunicationLog.objects.create(
                        customer=customer,
                        channel='whatsapp',
                        subject='WhatsApp Message',
                        content=message,
                        external_message_id=message_id,
                        is_outbound=True
                    )
                
                return True, message_id
            else:
                logger.error(f"WhatsApp API error: {response.text}")
                return False, response.text
                
        except Exception as e:
            logger.error(f"WhatsApp send error: {str(e)}")
            return False, str(e)
    
    def send_template_message(self, to_number, template_name, parameters, customer=None):
        """Send WhatsApp template message"""
        try:
            payload = {
                "messaging_product": "whatsapp",
                "to": to_number,
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {
                        "code": "en"
                    },
                    "components": [
                        {
                            "type": "body",
                            "parameters": [{"type": "text", "text": param} for param in parameters]
                        }
                    ]
                }
            }
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                f"{self.api_url}/{self.phone_number_id}/messages",
                json=payload,
                headers=headers
            )
            
            return response.status_code == 200, response.json()
            
        except Exception as e:
            logger.error(f"WhatsApp template send error: {str(e)}")
            return False, str(e)

class EmailService:
    """Email service for sending notifications and marketing emails"""
    
    def send_email(self, to_email, subject, content, customer=None, html_content=None):
        """Send email using Django's email backend"""
        try:
            from django.core.mail import EmailMultiAlternatives
            
            msg = EmailMultiAlternatives(
                subject=subject,
                body=content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[to_email]
            )
            
            if html_content:
                msg.attach_alternative(html_content, "text/html")
            
            result = msg.send()
            
            # Log communication
            if customer:
                CommunicationLog.objects.create(
                    customer=customer,
                    channel='email',
                    subject=subject,
                    content=content,
                    is_outbound=True
                )
            
            return result > 0, "Email sent successfully"
            
        except Exception as e:
            logger.error(f"Email send error: {str(e)}")
            return False, str(e)
    
    def send_bulk_email(self, customers, subject, content, html_content=None):
        """Send bulk emails to multiple customers"""
        results = []
        for customer in customers:
            if customer.email and customer.marketing_consent:
                success, message = self.send_email(
                    customer.email, 
                    subject, 
                    content, 
                    customer, 
                    html_content
                )
                results.append({
                    'customer_id': customer.id,
                    'email': customer.email,
                    'success': success,
                    'message': message
                })
        return results

class WeChatService:
    """
    WeChat API Integration
    Using WeChat Work API for business communications
    """
    
    def __init__(self):
        self.corp_id = settings.WECHAT_CORP_ID
        self.corp_secret = settings.WECHAT_CORP_SECRET
        self.agent_id = settings.WECHAT_AGENT_ID
        self.access_token = None
    
    def get_access_token(self):
        """Get WeChat access token"""
        try:
            url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
            params = {
                'corpid': self.corp_id,
                'corpsecret': self.corp_secret
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if data.get('errcode') == 0:
                self.access_token = data.get('access_token')
                return True
            else:
                logger.error(f"WeChat token error: {data}")
                return False
                
        except Exception as e:
            logger.error(f"WeChat token request error: {str(e)}")
            return False
    
    def send_message(self, to_user, message, customer=None):
        """Send WeChat message"""
        try:
            if not self.access_token:
                if not self.get_access_token():
                    return False, "Failed to get access token"
            
            url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.access_token}"
            
            payload = {
                "touser": to_user,
                "msgtype": "text",
                "agentid": self.agent_id,
                "text": {
                    "content": message
                }
            }
            
            response = requests.post(url, json=payload)
            data = response.json()
            
            if data.get('errcode') == 0:
                # Log communication
                if customer:
                    CommunicationLog.objects.create(
                        customer=customer,
                        channel='wechat',
                        subject='WeChat Message',
                        content=message,
                        external_message_id=data.get('msgid'),
                        is_outbound=True
                    )
                return True, "Message sent successfully"
            else:
                logger.error(f"WeChat send error: {data}")
                return False, data.get('errmsg', 'Unknown error')
                
        except Exception as e:
            logger.error(f"WeChat send error: {str(e)}")
            return False, str(e)

class CommunicationManager:
    """Unified communication manager"""
    
    def __init__(self):
        self.whatsapp = WhatsAppService()
        self.email = EmailService()
        self.wechat = WeChatService()
    
    def send_message(self, customer, channel, subject, content):
        """Send message via specified channel"""
        try:
            if channel == 'email' and customer.email:
                return self.email.send_email(customer.email, subject, content, customer)
            
            elif channel == 'whatsapp' and customer.whatsapp_number:
                return self.whatsapp.send_message(customer.whatsapp_number, content, customer)
            
            elif channel == 'wechat' and customer.wechat_id:
                return self.wechat.send_message(customer.wechat_id, content, customer)
            
            else:
                return False, f"No valid {channel} contact for customer"
                
        except Exception as e:
            logger.error(f"Communication error: {str(e)}")
            return False, str(e)
    
    def send_course_reminder(self, enrollment):
        """Send course reminder to enrolled customer"""
        customer = enrollment.customer
        course = enrollment.course
        
        subject = f"Reminder: {course.title} starts soon!"
        content = f"""
        Dear {customer.first_name},
        
        This is a reminder that your course "{course.title}" is starting soon.
        
        Start Date: {course.start_date.strftime('%Y-%m-%d %H:%M')}
        Duration: {course.duration_hours} hours
        
        Please ensure you're prepared for the session.
        
        Best regards,
        Learning Institute Team
        """
        
        return self.send_message(
            customer, 
            customer.preferred_communication, 
            subject, 
            content
        )
    
    def send_welcome_message(self, customer):
        """Send welcome message to new customer"""
        subject = "Welcome to Our Learning Institute!"
        content = f"""
        Dear {customer.first_name},
        
        Welcome to our learning community! We're excited to have you join us.
        
        You can explore our courses and upcoming conferences through our platform.
        
        If you have any questions, feel free to reach out to us.
        
        Best regards,
        Learning Institute Team
        """
        
        return self.send_message(
            customer, 
            customer.preferred_communication, 
            subject, 
            content
        )
