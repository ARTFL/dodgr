"""The application's Globals object"""

import loaders
import dico


class Globals(object):

    """Globals acts as a container for objects available throughout the
    life of the application

    """

    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the
        'app_globals' variable

        """
        loader = loaders.Separated('/w/artfl/projects/'
                            'dodgr/data/test/test.tab')
        self.dico = dico.Simple(loader)
