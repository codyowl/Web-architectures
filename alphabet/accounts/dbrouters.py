from accounts.models import Company

class CustomDBRouter(object):

    def db_for_read(self, model, **hints):
        """ reading SomeModel from otherdb """
        if model == Company:
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        """ writing SomeModel to otherdb """
        if model == Company:
            return 'default'
        return None
