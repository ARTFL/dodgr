"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper


def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE

    map.connect('/', controller='dodgrdico', action='home')
    map.connect('/s', controller='dodgrdico', action='lookup')
    map.connect('define', '/mot/{word}', controller='dodgrdico',
                action='define')
    map.connect('contribute', '/soumissions/', controller='usersub', action='index')
    map.connect('/soumissions/new/{word}', controller='usersub', action='index')
    map.connect('/soumissions/submit', controller='usersub', action='submit')
    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')
    map.connect('apropos', '/apropos', controller='dodgrdico', action='apropos')
    
    # STATIC ROUTES

    map.connect('jquery',
        'http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js',
         _static=True)

    # Redirect the trailing-slash version to no slash, which should be the
    # canonical URL
    map.redirect('/*(url)/', '/{url}',
                 _redirect_code='301 Moved Permanently')

    return map
