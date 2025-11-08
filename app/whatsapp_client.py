"""
Twilio WhatsApp Client
Handles sending and receiving WhatsApp messages via Twilio
"""
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from config import Config
from typing import Optional


class WhatsAppClient:
    """Client for Twilio WhatsApp integration"""
    
    def __init__(self):
        self.account_sid = Config.TWILIO_ACCOUNT_SID
        self.auth_token = Config.TWILIO_AUTH_TOKEN
        self.whatsapp_number = Config.TWILIO_WHATSAPP_NUMBER
        
        # Initialize Twilio client if credentials available
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
        else:
            self.client = None
            print("⚠️ Twilio credentials not configured")
    
    def send_message(self, to: str, body: str) -> bool:
        """
        Send a WhatsApp message
        
        Args:
            to: Recipient WhatsApp number (format: whatsapp:+1234567890)
            body: Message text
            
        Returns:
            True if sent successfully
        """
        if not self.client:
            print(f"[DEMO MODE] Would send to {to}: {body}")
            return False
        
        try:
            # Ensure 'to' has whatsapp: prefix
            if not to.startswith('whatsapp:'):
                to = f'whatsapp:{to}'
            
            message = self.client.messages.create(
                from_=self.whatsapp_number,
                body=body,
                to=to
            )
            
            print(f"✅ Message sent: {message.sid}")
            return True
        
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return False
    
    def send_message_with_media(
        self,
        to: str,
        body: str,
        media_url: str
    ) -> bool:
        """
        Send a WhatsApp message with media
        
        Args:
            to: Recipient WhatsApp number
            body: Message text
            media_url: URL of media to send
            
        Returns:
            True if sent successfully
        """
        if not self.client:
            print(f"[DEMO MODE] Would send to {to} with media: {body}")
            return False
        
        try:
            if not to.startswith('whatsapp:'):
                to = f'whatsapp:{to}'
            
            message = self.client.messages.create(
                from_=self.whatsapp_number,
                body=body,
                media_url=[media_url],
                to=to
            )
            
            print(f"✅ Message with media sent: {message.sid}")
            return True
        
        except Exception as e:
            print(f"❌ Error sending message with media: {e}")
            return False
    
    def create_response(self, message: str) -> str:
        """
        Create TwiML response for incoming message
        Used in webhook responses
        
        Args:
            message: Response message text
            
        Returns:
            TwiML string
        """
        response = MessagingResponse()
        response.message(message)
        return str(response)
    
    def parse_incoming_message(self, request_data: dict) -> dict:
        """
        Parse incoming Twilio webhook request
        
        Args:
            request_data: Request data from Twilio webhook
            
        Returns:
            {
                'from': str,  # User's WhatsApp number
                'body': str,  # Message text
                'media': list,  # Media URLs if any
                'location': tuple or None  # (lat, lng) if shared
            }
        """
        from_number = request_data.get('From', '')
        body = request_data.get('Body', '')
        
        # Parse media
        media_count = int(request_data.get('NumMedia', 0))
        media_urls = []
        for i in range(media_count):
            media_url = request_data.get(f'MediaUrl{i}')
            if media_url:
                media_urls.append(media_url)
        
        # Parse location if shared
        latitude = request_data.get('Latitude')
        longitude = request_data.get('Longitude')
        location = None
        if latitude and longitude:
            try:
                location = (float(latitude), float(longitude))
            except (ValueError, TypeError):
                location = None
        
        return {
            'from': from_number,
            'body': body,
            'media': media_urls,
            'location': location
        }


# Singleton instance
whatsapp_client = WhatsAppClient()
