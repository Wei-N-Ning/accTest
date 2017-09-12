
ozArea = '/olympus/shots/testing/002'


class TestPublishCharMap(object):
    hydraGroup = '/olympus/shots/testing/002'
    productType = 'genFile'
    productName = 'charMapForDemo'

    tasks = [
        'GenerateCharMap',
        'PublishCharMap',
        'AssertCharMapPublish'
    ]
