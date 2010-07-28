"""The application's Globals object"""
import cPickle
import dico
import dico.mappers


class Globals(object):

    """Globals acts as a container for objects available throughout the
    life of the application

    """

    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the
        'app_globals' variable

        """
        # TODO: paths should live in config somewhere
        pickle = open('/w/artfl/corpora/idol/dico_pickles/latest.pickle')
        self.dico = cPickle.load(pickle)
        pickle.close()