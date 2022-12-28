import re
from flask import request, jsonify, url_for, g
from app.extensions import db
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request
from flask_babel import gettext as _
import os, uuid
import os.path as op
from werkzeug import secure_filename
import app

from app.models import Visit, Attachment




BASE_DIR = '/var/www/yanei/uploads/'
BASE_URL = 'http://yanei.miaohf.com/uploads/'

UPLOADTYPES = ['png', 'jpg', 'jpeg']


@bp.route('/upload', methods=['POST'])
# @token_auth.login_required
def upload():

    id = request.args.get('id', type=int)
    type = request.args.get('filetype')

    

    file = request.files['file']
    filename = file.filename
    
    # Gen GUUID File Name
    fileExt = filename.split('.')[-1]
    

    if fileExt in UPLOADTYPES:
        

        # Save file Info into DB
        visit = Visit.query.get_or_404(id)

        CUSTOMERID = str(visit.customer_id)
        UPLOADDIR = BASE_DIR + CUSTOMERID + '/'

        print(UPLOADDIR)
        
        if not os.path.isdir(UPLOADDIR):
            os.mkdir(UPLOADDIR)

        FILENAME = str(uuid.uuid4()) + '.' + fileExt
        URI = BASE_URL + CUSTOMERID + '/' + FILENAME
        file.save(os.path.join(UPLOADDIR , FILENAME))


        new_attach = Attachment()
        new_attach.uri = URI
        db.session.add(new_attach)
        visit.attachments.append(new_attach)

    db.session.commit()

    return ('OK')



@bp.route('/remove', methods=['DELETE'])
# @token_auth.login_required
def delete_file():
    pass
    return ('OK')
