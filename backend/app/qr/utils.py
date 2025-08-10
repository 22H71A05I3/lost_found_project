# Utility functions for creating QR codes from text or URLs, saving images, and encoding QR data.
import qrcode
from io import BytesIO
import base64
import os

def create_qr_code(data):
	"""Create a QR code image from text or URL."""
	qr = qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_L,
		box_size=10,
		border=4,
	)
	qr.add_data(data)
	qr.make(fit=True)
	img = qr.make_image(fill_color="black", back_color="white")
	return img

def save_qr_image(img, filename):
	"""Save QR code image to a file."""
	img.save(filename)
	return filename

def encode_qr_to_data_url(img):
	"""Encode QR code image to a base64 data URL."""
	buf = BytesIO()
	img.save(buf, format='PNG')
	buf.seek(0)
	data_url = "data:image/png;base64," + base64.b64encode(buf.read()).decode('utf-8')
	return data_url

