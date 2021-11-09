from django import forms

from authentication.models import User

from . import models


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Review
        fields = ['rating', 'headline', 'body']


class DeleteReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput,
                                       initial=True)


class FollowForm(forms.ModelForm):
    class Meta:
        model = models.UserFollows
        fields = ['user', 'followed_user']


class SubscriptionForm(forms.Form):
    following = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={
                                    'placeholder': 'Username'
                                }))

    def clean_following(self):
        following = self.cleaned_data['following']
        if not User.objects.filter(username=following).exists():
            raise forms.ValidationError('User does not exist')
        return following

    def existing(self, userconnected):
        try:
            user = User.objects.get(
                username=self.cleaned_data.get('following'))
            models.UserFollows.objects.get(user=userconnected,
                                           following_id=user)
            return True
        finally:
            return False
