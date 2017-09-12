

class RunnerInterface(object):

    def run(self, dslFilePath):
        """
        Given a dsl document file path, creates the fixture objects and execute them one by one

        Args:
            dslFilePath (str):

        """
        raise NotImplementedError

    def initialize(self):
        """
        If there is anything to be initialized on the client side, do it here; It is optional in some cases
        """
        pass
