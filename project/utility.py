import os
from project import app, db
from PIL import Image
from flask import url_for
from flask_login import current_user
from project.models import User


def remove_unused_images():
    pic_dir = os.path.join(app.root_path, 'static/profile_pics')

    pic_filenames = []
    for filename in os.listdir(pic_dir):    # os.listdir List all directory and files
        if os.path.isfile(os.path.join(pic_dir, filename)):
            pic_filenames.append(filename)

    db_filenames = [user.image_file for user in User.query.all()]

    unused_filenames = []
    for filename in pic_filenames:
        if filename not in db_filenames:
            unused_filenames.append(filename)

    unused_filenames = set(unused_filenames)

    unused_filenames.discard('default.jpg')  # exclude default.jpg file from deletion
    for filename in unused_filenames:
        os.remove(os.path.join(pic_dir, filename)) #os.path.join combining the 2 filepath


def parse_price(choice):
    prices = {
            'Haircut with Style': 150,
            'Haircut Trim': 100,
            'Manicure': 100,
            'Pedicure': 100,
            'Manicure Gel': 800,
            'Ordinary Manicure': 600,
            'Pedicure Gel': 800,
            'Pedicure Ordinary': 600,
            'Footspa': 250,
            'Footspa with Foot Reflex': 450,
            'Footspa with Footmask': 250,
            'Footspa with Gel': 300,
            '1 Hour Massage': 300,
            '1 1/2 Massage': 450,
            '2 Hours Massage': 250,
            '1 Hour Massage with Hot Compress': 350,
            '1 1/2 Hour Massage with Hot Compress': 500,
            '2 Hours Massage with Hot Compress': 700,
            '1 Hour Massage with Hot Stone': 400,
            '1 1/2 Hour Massage with Hot Stone': 600,
            '2 Hours Massage with Hot Stone': 800,
            '2 Hour Massage with Ventosa': 800,
            '1 1/2 Hour Massage with Ventosa': 600,
            '30 Mins FootReflex': 200,
            '1 Hour FootReflex': 400,
            'Ear Candle Only': 200,
            '1 1/2 Hour Body Scrub with Massage': 600,
            '2 Hours Body Scrube with Massage': 900,
            'Whitening': 350,
            'Waxing Underarm': 300,
            'Waxing Legs': 600,
            'Waxing Bikini': 200,
            'Eyelash Extension': 800,
            'Eyelash Firming': 300,
            'Eyebrow Threading': 200,
            'Eyebrow Shaving': 100,
            'Traditional Hair & Make-up': 800,
            'Air Brush Make-up': 1500

    }

    return prices.get(choice, 0.00)  # Return the price based on the choice, or 0.00 if not found