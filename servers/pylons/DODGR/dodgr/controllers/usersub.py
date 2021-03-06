import logging
import MySQLdb

from pylons import config, request, response, session, tmpl_context as c
from pylons import app_globals
from pylons.controllers.util import abort, redirect

from dodgr.lib.base import BaseController, render

from recaptcha.client.captcha import displayhtml, submit as submit_captcha

log = logging.getLogger(__name__)


class UsersubController(BaseController):

    def index(self, word=None):
        """Default action: render the template that allows a user to submit a
        definition"""
        c.word = word
        c.recaptcha = displayhtml(config['recaptcha.public_key'])
        return render('/userdef_submit.html')

    def submit(self):
        """Handle the submission of a definition"""

        # First, check if the recaptcha is correct
        recaptcha_challenge_field = request.POST.get(
                                    'recaptcha_challenge_field', None)
        recaptcha_response_field = request.POST.get(
                                   'recaptcha_response_field', None)
        remoteip = request.environ.get('REMOTE_ADDR', None)
        recaptcha_response = submit_captcha(recaptcha_challenge_field,
                                            recaptcha_response_field,
                                            config['recaptcha.private_key'],
                                            remoteip)
        print recaptcha_response.is_valid
        print recaptcha_response.error_code
        if not recaptcha_response.is_valid:
            c.recaptcha = displayhtml(config['recaptcha.public_key'],
                                      error=recaptcha_response.error_code)
            return render('/userdef_submit.html')

        headword = request.params['headword']
        definition = request.params['definition'].encode('utf-8')

        # DB connection
        app_globals.db.insert(headword, definition, 'web')

        c.word = headword
        return render('/userdef_success.html')
