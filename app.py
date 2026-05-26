from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
CORS(app)  # Allows your frontend website to securely talk to this backend

# --- EMAIL CONFIGURATION ---
SENDER_EMAIL = "makgurav82@gmail.com"
# For Gmail, you MUST use an "App Password", not your regular password.
# (See instructions below on how to generate this)
SENDER_PASSWORD = "jgdzteqatpdhlmuc" 
RECEIVER_EMAIL = "makgurav82@gmail.com"

def send_order_email(order_data):
    try:
        # Create message container
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f"🚨 New Order Received: {order_data['id']}"

        # Construct a beautiful email body text
        body = f"""
        New Order Alert for The Green Thumb! 🌾
        -------------------------------------------
        Order ID: {order_data['id']}
        Customer Name: {order_data['customer']}
        Phone Number: {order_data['phone']}
        Shipping Address: {order_data['address']}
        
        Items Manifest:
        {order_data['items']}
        
        -------------------------------------------
        Total Amount: ₹{order_data['total']:.2f}
        """
        
        msg.attach(MIMEText(body, 'plain'))

        # Connect to Gmail's secure SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Encrypt the connection
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        # Send the email
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print(f"Success: Email sent for order {order_data['id']}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@app.route('/api/orders', methods=['POST'])
def receive_order():
    order_data = request.json
    
    # 1. Trigger the background email process
    email_success = send_order_email(order_data)
    
    if email_success:
        return jsonify({"status": "success", "message": "Order processed and email alert sent!"}), 200
    else:
        return jsonify({"status": "partial_error", "message": "Order captured locally, but email failed."}), 500

if __name__ == '__main__':
    # Runs the server locally on port 5000
    app.run(debug=True, port=5000)