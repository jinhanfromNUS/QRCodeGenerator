from flask import Flask, render_template, request, send_file, redirect, url_for
import qrcode
from io import BytesIO
import os

app = Flask(__name__)

# Directory to store temporary QR code images
TEMP_DIR = 'static/temp_qr_codes'
os.makedirs(TEMP_DIR, exist_ok=True)  # Ensure the directory exists

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    # Get the form data (URL, QR code color, and background color)
    data = request.form['qr_data']
    qr_color = request.form['qr_color']
    bg_color = request.form['bg_color']

    # Create the QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add the data to the QR code
    qr.add_data(data)
    qr.make(fit=True)

    # Create the image with the specified colors
    img = qr.make_image(fill_color=qr_color, back_color=bg_color)

    # Create a unique filename for the QR code
    qr_filename = f"{data[:10].replace('/', '_').replace(' ', '_')}.png"
    qr_filepath = os.path.join(TEMP_DIR, qr_filename)

    # Save the QR code image
    img.save(qr_filepath)

    # Redirect to the route that displays the QR code and pass the original text/link
    return redirect(url_for('display_qr', filename=qr_filename, qr_text=data))


@app.route('/display_qr/<filename>')
def display_qr(filename):
    # Retrieve the original data from the query parameters
    qr_text = request.args.get('qr_text')

    # Display the QR code stored in the temporary directory
    return render_template(
        'display_qr.html', 
        qr_image=f"{url_for('static', filename=f'temp_qr_codes/{filename}')}",
        qr_text=qr_text  # Pass the link/text to the template
    )


if __name__ == '__main__':
    app.run(debug=True)
