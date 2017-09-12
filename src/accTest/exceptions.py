

class MissingProperty(Exception):

    def __init__(self, name):
        super(MissingProperty, self).__init__(
            'Property: {} does not exist on fixture'.format(name)
        )


class BrokenTask(Exception):

    def __init__(self, task):
        super(Exception, self).__init__(
            'Task {} is not associated with any fixture (orphaned task).'.format(task.fullName())
        )


class CanNotLoadTask(Exception):

    def __init__(self, filePath, dslTaskName, msg=''):
        super(CanNotLoadTask, self).__init__(
            'Can not load task!\nSearch path: {}, Task: {}\nReason: {}'.format(filePath, dslTaskName, msg)
        )


class MalformedTaskName(Exception):

    def __init__(self, dslTaskName):
        super(MalformedTaskName, self).__init__(
            'Only name that contains $TYPE or $TYPE:$INSTANCE is supported! Got: {}'.format(dslTaskName)
        )


class InvalidDslFilePath(Exception):

    def __init__(self, dslFilePath):
        super(InvalidDslFilePath, self).__init__(
            'Invalid dsl document file path: {}'.format(dslFilePath)
        )