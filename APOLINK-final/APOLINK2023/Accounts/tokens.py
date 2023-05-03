from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


#This file let you to generate a token password reset system, don't touch that
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk)+ six.text_type(timestamp) + six.text_type(user.is_active)

#create an object to activate the token
account_activation_token = AccountActivationTokenGenerator()