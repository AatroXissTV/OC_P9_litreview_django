from .models import Review, Ticket, UserFollows


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


def check_tickets_reply(userid, tickets_feed):
    reviews = Review.objects.filter(user_id=userid)
    tickets_reply_id = []
    for review in reviews:
        tickets_reply_id.append(review.ticket_id)

    return(tickets_reply_id)
