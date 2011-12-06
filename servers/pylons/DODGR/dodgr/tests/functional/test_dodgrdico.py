from dodgr.tests import *

class TestDodgrdicoController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='dodgrdico', action='index'))
        # Test response...
