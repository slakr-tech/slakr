import views.posts.post_database as pdb
import views.follow.follow_database as fdb
import user_database as db

def get_feed(user):
    if not db.get_user(user, '_id'):
        return 'user not found'

    following_statuses = fdb.get_following(user)
    posts = []
    users = [following_status['following'] for following_status in following_statuses]
    for i in pdb.get_posts_by_multiple_users(users):
        posts.append(i)
    if posts:
        if len(posts) < 50:
            return posts
        return posts[:50]
    else:
        return False