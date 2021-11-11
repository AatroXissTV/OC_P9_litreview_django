from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from . import forms
from . import models


@login_required
def home(request):
    tickets = models.Ticket.objects.all()
    reviews = models.Review.objects.all()
    return render(request, 'app/home.html', context={'tickets': tickets,
                                                     'reviews': reviews})


@login_required
def create_ticket(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            # set the uploader to the user before saving the model
            ticket.user = request.user
            # now we can save
            ticket.save()
            return redirect('home')
    return render(request, 'app/create_ticket.html', context={'form': form})


@login_required
def create_review(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')
    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
    }
    return render(request, 'app/create_review.html', context=context)


@login_required
def view_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    return render(request, 'app/view_review.html', context={'review': review})


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    edit_review = forms.ReviewForm(instance=review)
    delete_review = forms.DeleteReviewForm()
    if request.method == 'POST':
        if 'edit_review' in request.POST:
            edit_review = forms.ReviewForm(request.POST, instance=review)
            if edit_review.is_valid():
                edit_review.save()
                return redirect('home')
        if 'delete_review' in request.POST:
            delete_review = forms.DeleteReviewForm(request.POST)
            if delete_review.is_valid():
                review.delete()
                return redirect('home')
    context = {
        'edit_review': edit_review,
        'delete_review': delete_review,
    }
    return render(request, 'app/edit_review.html', context=context)


User = get_user_model()


@login_required
def sub(request):

    users = []
    follows = []
    followed_by = []

    if models.UserFollows.objects.filter(user=request.user):
        for entry in models.UserFollows.objects.filter(user=request.user):
            follows.append(entry.followed_user)
    if models.UserFollows.objects.filter(followed_user=request.user):
        for entry in models.UserFollows.objects.filter(
            followed_user=request.user
        ):
            followed_by.append(entry.user)
    users = [user for user in User.objects.all()
             if user not in follows and user != request.user]

    if request.method == 'GET':
        context = {
            'users': users,
            'follows': follows,
            'followed_by': followed_by,
        }
        return render(request, 'app/sub.html', context=context)

    if request.method == 'POST':
        if request.POST.get('follow'):
            follow = models.UserFollows(
                user=request.user,
                followed_user=User.objects.get(id=request.POST.get('follow'))
            )
            follow.save()
            return redirect('sub')

    elif request.POST.get('unfollow'):
        unfollow = models.UserFollows.objects.filter(
            user=request.user,
            followed_user=User.objects.get(id=request.POST.get('unfollow'))
        )
        unfollow.delete()
        return redirect('sub')
