from flask.ext.login import UserMixin, AnonymousUserMixin

class User(UserMixin):
    _quotas = None
    def __init__(self, email):
        self.email = email

    def is_authenticated(self):
        return self.email != None

    def is_authorized(self):
        return self.email.endswith('mozilla.com') or self.email.endswith('mozilla.org')

    def is_active(self):
        return self.email != None

    def is_anonymous(self):
        return self.email == None

    def get_id(self):
        return self.email

    def get_max_workers(self,dflt):
        return _quotas['users'].get(self.email,dflt)

    def is_worker_count_valid(self,asked,dflt):
        if asked > _quotas['users'].get(self.email, dflt) or asked <=0:
            return False
        else:
            return True

class AnonymousUser(AnonymousUserMixin):
    def is_authorized(self):
        return False
