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
        # TODO: pickle location should be in config somewhere
        pickle_file = '/w/artfl/corpora/stack_pickles/latest.pickle'
        pickle_handle = open(pickle_file, 'r')
        self.stack = cPickle.load(pickle_handle)
        pickle_handle.close()
