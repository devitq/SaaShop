from django.contrib.auth.tokens import PasswordResetTokenGenerator

__all__ = ("AccountActivationTokenGenerator",)


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.is_active)


account_activation_token = AccountActivationTokenGenerator()
