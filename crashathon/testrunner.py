from green.djangorunner import DjangoRunner


class TestRunner(DjangoRunner):
    """
    A test suite runner that does not set up and tear down a database.
    """

    def setup_databases(self):
        pass

    def teardown_databases(self, *args):
        pass
