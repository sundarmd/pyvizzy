from flask import Flask, request, jsonify
import logging
import email_validator

# Assuming these modules are implemented similarly to their Go counterparts
from files import get_file_manager
from keys import get_email_key

app = Flask(__name__)
logging.basicConfig(level=logging.ERROR)

@app.route('/save-email', methods=['POST'])
def save_email():
    s3 = get_file_manager()

    email = request.args.get('email')
    
    try:
        # Validate email
        email_validator.validate_email(email)
    except email_validator.EmailNotValidError as e:
        logging.error(str(e))
        return jsonify({"error": "Invalid email"}), 400

    try:
        s3.write_file(get_email_key(email), email.encode('utf-8'))
    except Exception as e:
        logging.error(f"Failed to save email: {str(e)}")
        return jsonify({"error": "Failed to save email"}), 500

    return jsonify({"success": True}), 200

if __name__ == '__main__':
    app.run(debug=True)

	# make sure to install theese dependancies
	#pip install flask email_validator