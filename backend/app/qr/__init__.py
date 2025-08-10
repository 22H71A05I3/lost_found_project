from flask import Blueprint, send_from_directory, current_app

qr_bp = Blueprint('qr', __name__)

# API route to retrieve QR code image for an item
@qr_bp.route('/qr_codes/<filename>', methods=['GET'])
def get_qr_code(filename):
	qr_dir = os.path.join(os.path.dirname(__file__), '../../static/qr_codes')
	return send_from_directory(qr_dir, filename)

def init_qr(app):
	app.register_blueprint(qr_bp, url_prefix='/api')

import qrcode
import os

def generate_qr_for_item(item_id, info_url):
	"""
	Generate a QR code for the found item, linking to info_url (e.g., item details page).
	Saves the QR code image to a static/qr_codes directory.
	"""
	qr = qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_L,
		box_size=10,
		border=4,
	)
	qr.add_data(info_url)
	qr.make(fit=True)
	img = qr.make_image(fill_color="black", back_color="white")
	qr_dir = os.path.join(os.path.dirname(__file__), '../../static/qr_codes')
	os.makedirs(qr_dir, exist_ok=True)
	img_path = os.path.join(qr_dir, f"item_{item_id}.png")
	img.save(img_path)
	return img_path
