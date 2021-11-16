# django imports
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignupFrom(UserCreationForm):
    """ This class represents the signup form. """
    def __init__(self, *args, **kwargs):
        super(SignupFrom, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')
