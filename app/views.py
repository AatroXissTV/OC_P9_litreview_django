# django imports
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Value, CharField
from django.shortcuts import render, redirect, get_object_or_404

# local imports
from .forms import DeleteReviewForm, TicketForm, ReviewForm
from .models import Ticket, Review, UserFollows
from .getfeed import get_reviews_for_feed, get_tickets_for_feed
from .getfeed import check_tickets_reply

# third party imports
from itertools import chain

""" All views for the app are behind decorator @login_required """

# get the user model
User = get_user_model()


@login_required
def feed(request):
    """ Represent the feed page of the user """

    # get reviews for feed
    reviews = get_reviews_for_feed(request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    # get tickets for feed
    tickets = get_tickets_for_feed(request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    # chain reviews & tickets and sort by time_created
    feed = sorted(
        chain(reviews, tickets),
        key=lambda x: x.time_created,
        reverse=True)
    tlfr = []
    for review in reviews:
        tlfr.append(review.ticket.id)
    ticket_list_for_review = Ticket.objects.filter(id__in=tlfr)

    # Initialize context
    context = {
        'feed': feed,
        'ticket_list_for_review': ticket_list_for_review,
        'users': User.objects.all(),
        'ticket_id_reply': check_tickets_reply(request.user, tickets)
    }
    return render(request, 'app/feed.html', context)


@login_required
def create_ticket(request):
    """ Represent the create ticket page of the user """

    form = TicketForm()
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('feed')

    return render(request, 'app/create_ticket.html', {'form': form})


@login_required
def create_review(request):
    """ Represents the create review page of the user """

    ticket_form = TicketForm()
    review_form = ReviewForm()
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('feed')

    # Initialize context
    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
    }
    return render(request, 'app/create_review.html', context=context)


@login_required
def create_review_response(request, ticket_id):
    ticket_obj = get_object_or_404(Ticket, id=ticket_id)
    review_form = ReviewForm()
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            Review.objects.create(
                headline=request.POST['headline'],
                body=request.POST['body'],
                user=request.user,
                ticket=ticket_obj,
                rating=request.POST['rating']
            )
            return redirect('feed')

    # Initialize context
    context = {
        'review_form': review_form,
        'infos_ticket': ticket_obj,
        'ticket': Ticket.objects.get(id=ticket_id),
    }

    return render(request, 'app/create_review_response.html', context=context)


@login_required
def edit_review(request, review_id):
    """ Represents the edit review page of the user """

    review = get_object_or_404(Review, id=review_id)
    edit_review = ReviewForm(instance=review)
    delete_review = DeleteReviewForm()
    if request.method == 'POST':
        # check if edit_review is in request.POST
        if 'edit_review' in request.POST:
            edit_review = ReviewForm(request.POST, instance=review)
            if edit_review.is_valid():
                edit_review.save()
                return redirect('feed')
        # check if delete_review is in request.POST
        if 'delete_review' in request.POST:
            delete_review = DeleteReviewForm(request.POST)
            if delete_review.is_valid():
                review.delete()
                return redirect('feed')

    # Initialize context
    context = {
        'edit_review': edit_review,
        'delete_review': delete_review,
    }
    return render(request, 'app/edit_review.html', context=context)


@login_required
def view_review(request, review_id):
    """ Represent the view review page of the user """
    review = get_object_or_404(Review, id=review_id)

    return render(request, 'app/view_review.html', context={'review': review})


@login_required
def display_follow(request):
    """Display follows subscription & followers to the user"""

    # Initialize lists
    follows = []
    followers = []
    # Get follows
    if UserFollows.objects.filter(user=request.user):
        for entry in UserFollows.objects.filter(user=request.user):
            follows.append(entry.followed_user)
    # Get followers
    if UserFollows.objects.filter(followed_user=request.user):
        for entry in UserFollows.objects.filter(followed_user=request.user):
            followers.append(entry.user)

    # Display follows & followers
    if request.method == 'GET':
        context = {
            'follows': follows,
            'followers': followers,
        }

    elif request.method == 'POST':
        if request.POST.get('follow'):
            context = {
                'follows': follows,
                'followers': followers,
            }
            follow(request)
            return redirect('follow')

        elif request.POST.get('unfollow'):
            context = {
                'follows': follows,
                'followers': followers,
            }
            unfollow(request)
            return redirect('follow')
    return render(request, 'app/follow.html', context=context)


@login_required
def follow(request):
    """ follow a user """
    searched = request.POST['follow']
    try:
        user = User.objects.get(username=searched)
        new_follow = UserFollows(user=request.user, followed_user=user)
        new_follow.save()
    except User.DoesNotExist:
        print('User does not exist')


@login_required
def unfollow(request):
    """ Unfollow a user """

    unfollow = UserFollows.objects.filter(
        user=request.user,
        followed_user=User.objects.get(id=request.POST.get('unfollow'))
    )
    unfollow.delete()
