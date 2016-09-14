
import os


class Builder(object):

    def __init__(self):
        pass

    def build(self, filename):
        os.system('./node_modules/pug-cli/index.js %s' % filename)


STANDARD_BUILDER = Builder()
