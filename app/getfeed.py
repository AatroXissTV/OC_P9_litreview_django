from .models import Review, Ticket, UserFollows


def get_number_of_reviews(userid):

    # Initialize the number of reviews
    number_of_reviews = 0

    # query user reviews
    query_reviews = Review.objects.filter(user_id=userid)
    for q_review in query_reviews:
        number_of_reviews += 1

    return number_of_reviews


def get_reviews_for_feed(userid):
    followers = UserFollows.objects.filter(user_id=userid)
    followers_ids = [userid.id]
    for follower in followers:
        followers_ids.append(follower.followed_user_id)

    reviews_id = []
    query_reviews = Review.objects.filter(user_id__in=followers_ids).distinct()
    for q_review in query_reviews:
        reviews_id.append(q_review.id)

    self_tickets = Ticket.objects.filter(user_id=userid)
    for self_ticket in self_tickets:
        reply_reviews = Review.objects.filter(ticket_id=self_ticket.id)
        for reply_review in reply_reviews:
            reviews_id.append(reply_review.id)

    return(Review.objects.filter(id__in=reviews_id).distinct())


def get_tickets_for_feed(userid):
    followers = UserFollows.objects.filter(user_id=userid)
    followers_ids = [userid.id]
    for follower in followers:
        followers_ids.append(follower.followed_user_id)

    return(Ticket.objects.filter(user_id__in=followers_ids).distinct())


def check_tickets_reply(userid, tickets):

    # Initialize tickets lists
    answered_tickets = []
    not_answered_tickets = []

    # Check if the ticket has a reply by a user
    for ticket in tickets:
        if ticket.user == userid:
            #  check if a review has the same user as the ticket
            q_reviews = Review.objects.filter(ticket_id=ticket.id)
            for review in q_reviews:
                if review.user == userid:
                    answered_tickets.append(ticket.id)
                else:
                    not_answered_tickets.append(ticket.id)
        else:
            not_answered_tickets.append(ticket.id)

    return(Ticket.objects.filter(id__in=answered_tickets).distinct(),
           Ticket.objects.filter(id__in=not_answered_tickets).distinct())
