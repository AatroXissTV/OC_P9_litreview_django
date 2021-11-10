from django import forms
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


class UserFollowsForm(forms.ModelForm):
    class Meta:
        model = models.UserFollows
        fields = [
            'followed_user'
        ]
