# django imports
from django import forms

# local imports
from . import models


class TicketForm(forms.ModelForm):
    """ Represents the form for creating a new ticket """

    edit_ticket = forms.BooleanField(widget=forms.HiddenInput(), initial=True)

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']


class DeleteTicketForm(forms.Form):
    """ Represents the form for deleting a ticket """

    delete_ticket = forms.BooleanField(widget=forms.HiddenInput,
                                       initial=True)


class ReviewForm(forms.ModelForm):
    """ Represents the form for creating a new review """

    rating = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)],
                               widget=forms.RadioSelect())
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Review
        fields = ['rating', 'headline', 'body']


class DeleteReviewForm(forms.Form):
    """ Represents the form for deleting a review """

    delete_review = forms.BooleanField(widget=forms.HiddenInput,
                                       initial=True)


class UserFollowsForm(forms.ModelForm):
    """ Represents the form for following a user """

    class Meta:
        model = models.UserFollows
        fields = [
            'followed_user'
        ]
