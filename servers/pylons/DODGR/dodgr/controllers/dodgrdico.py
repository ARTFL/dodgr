import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from dodgr.lib.base import BaseController, render

import loaders
import dico

log = logging.getLogger(__name__)


class DodgrdicoController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/dodgrdico.mako')
        # or, return a response
        return 'Hello World'

    def define(self, word):
        """Load up the test dictionary and serve the definition, if any, for
        the word defined in the route"""
        loader = loaders.Separated('/w/artfl/projects/'
                            'dodgr/data/test/test.tab')
        test_dico = dico.Simple(loader)
        definition = test_dico.define(word)
        if definition:
            return "Entry :", definition
        else:
            return "is undefined"
