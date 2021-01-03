import blueprints.posts.post_database as pdb
import blueprints.follow.follow_database as fdb
import user_database as db

def get_feed(user):
    if not db.get_user(user, '_id'):
        return 'user not found'

    following_statuses = fdb.get_following(user)
    posts = []

    for following_status in following_statuses:
        followed_user = db.get_user(following_status['following'], "_id")
        print(dir(followed_user))
        for i in pdb.get_posts(followed_user.id):
            posts.append(i)
    print('posts:')
    print(posts)
    if len(posts) < 50:
        return posts
    return posts[:50]