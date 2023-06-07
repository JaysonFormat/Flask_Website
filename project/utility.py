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
