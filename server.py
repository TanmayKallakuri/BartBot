"""
Flask Web Server for BARTBot
Handles Twilio webhooks and provides API endpoints
"""
from flask import Flask, request, Response
from flask_cors import CORS
from app.bot import bartbot
from app.whatsapp_client import whatsapp_client
from config import Config

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.config.from_object(Config)


@app.route('/')
def index():
    """Health check endpoint"""
    return {
        'status': 'ok',
        'service': 'BARTBot WhatsApp Service',
        'version': '1.0.0'
    }


@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Twilio webhook endpoint for incoming WhatsApp messages
    """
    try:
        # Parse incoming message
        incoming = whatsapp_client.parse_incoming_message(request.form.to_dict())
        
        user_id = incoming['from']
        message_text = incoming['body']
        location = incoming['location']
        
        print(f"\n📱 Incoming message from {user_id}:")
        print(f"   Message: {message_text}")
        if location:
            print(f"   Location: {location}")
        
        # Process message with bot
        response_text = bartbot.process_message(user_id, message_text, location)
        
        print(f"🤖 Bot response: {response_text[:100]}...")
        
        # Create TwiML response
        twiml_response = whatsapp_client.create_response(response_text)
        
        return Response(twiml_response, mimetype='application/xml')
    
    except Exception as e:
        print(f"❌ Error processing webhook: {e}")
        
        # Send error message to user
        error_response = "Oops, something went wrong 😕\n\nTry again in a bit!"
        twiml_response = whatsapp_client.create_response(error_response)
        
        return Response(twiml_response, mimetype='application/xml')


@app.route('/send', methods=['POST'])
def send_message():
    """
    API endpoint to send a message (for testing or proactive messages)
    
    POST body:
    {
        "to": "whatsapp:+1234567890",
        "message": "Hello!"
    }
    """
    try:
        data = request.get_json()
        to = data.get('to')
        message = data.get('message')
        
        if not to or not message:
            return {'error': 'Missing to or message'}, 400
        
        success = whatsapp_client.send_message(to, message)
        
        if success:
            return {'status': 'sent'}
        else:
            return {'error': 'Failed to send'}, 500
    
    except Exception as e:
        return {'error': str(e)}, 500


@app.route('/stats', methods=['GET'])
def stats():
    """
    Get bot statistics
    """
    from app.utils.session_manager import session_manager
    
    active_sessions = session_manager.get_active_sessions_count()
    
    return {
        'active_sessions': active_sessions,
        'status': 'operational'
    }


if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("🚇 BARTBot WhatsApp Service")
    print("=" * 50)
    print("\nServer starting on http://127.0.0.1:5000")
    print("\nEndpoints:")
    print("  GET  /          - Health check")
    print("  POST /webhook   - Twilio webhook")
    print("  POST /send      - Send message")
    print("  GET  /stats     - Bot statistics")
    print("\n" + "=" * 50 + "\n")
    
    # Run server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=Config.DEBUG
    )
