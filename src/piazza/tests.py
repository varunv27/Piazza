import requests
import datetime
from django.test import TestCase

# Create your tests here.
host = 'http://10.61.64.83:8000/'


# reqistration function
def register(username, password):
    url = f"{host}auth/register/"
    data = {
        'username': username,
        'password': password
    }
    res = requests.post(url, data=data)
    return res.json()


# login function
def get_token(username, password):
    url = f"{host}auth/token/"
    data = {
        'username': username,
        'password': password
    }
    res = requests.post(url, data=data)
    return res.json()


# create post function
def create_post(token=None, topic=None, title=None, duration=0, body=''):
    url = f"{host}posts/"
    headers = {
        'Authorization': f'Bearer {token}'
    }

    time_change = datetime.timedelta(seconds=duration)
    expiry_date = datetime.datetime.now() + time_change

    data = {
        'topic': topic,
        'title': title,
        'expiry_date': expiry_date,
        'body': body
    }
    res = requests.post(url, headers=headers, data=data)
    return res.json()


def get_posts(token=None, topic='', status='', ordering='', activity=''):
    url = f"{host}posts/"
    params = {
        'topic': topic,
        'status': status,
        'ordering': ordering,
        'activity': activity
    }
    headers = {
        'Authorization': f'Bearer {token}'
    }
    res = requests.get(url, headers=headers, params=params)
    return res.json()


# get a single post function
def get_post(token=None, post_id=None):
    url = f"{host}posts/{post_id}/"

    headers = {
        'Authorization': f'Bearer {token}'
    }
    res = requests.get(url, headers=headers)
    return res.json()


# comment function
def comment(token=None, post_id=None, message=''):
    url = f"{host}posts/{post_id}/comments/"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    data = {
        'message': message
    }
    res = requests.post(url, headers=headers, data=data)
    return res.json()


def like(token, post_id):
    url = f"{host}posts/{post_id}/like/"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    res = requests.get(url, headers=headers)
    return res.json()


def dislike(token, post_id):
    url = f"{host}posts/{post_id}/dislike/"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    res = requests.get(url, headers=headers)
    return res.json()

'''
# TC 1 Olga, Nick, Mary and Nestor register and are ready to access the Piazza API
 print(register('olga', '1234567@'))
 print(register('nick', '1234567@'))
 print(register('mary', '1234567@'))
 print(register('nestor', '1234567@'))
'''


# TC 2 Olga, Nick, Mary and Nestor use the oAuth v2 authorisation service to get their tokens (registeration is handled in previous step)
olga = get_token('olga', '1234567@')
nick = get_token('nick', '1234567@')
mary = get_token('mary', '1234567@')
nestor = get_token('nestor', '1234567@')

'''
print(olga)
print(nick)
print(mary)
print(nestor)
'''


# TC 3 get post without token should fail
#print(get_posts())


#'''
# TC 4 Olga posts a message to Tech topic with an expiration time 60seconds
print(
    create_post(
        token=olga['access_token'], topic='tech',
        title="This is Olga's Tech topic",
        duration=60,
        body="This is Olga's TechThis is Olga's TechThis is Olga's TechThis is Olga's Tech"
    )
)
#'''

'''
# TC 5 Nick posts a message to Tech topic with an expiration time 60seconds
print(
    create_post(
        token=nick['access_token'], topic='tech',
        title="This is Nick's Tech topic",
        duration=60,
        body="This is Nick's TechThis is Nick's TechThis is Nick's TechThis is Nick's Tech"
    )
)
'''

'''
# TC 6 Mary posts a message to Tech topic with an expiration time 60seconds
print(
    create_post(
        token=mary['access_token'], topic='tech',
        title="This is Mary's Tech topic",
        duration=60,
        body="This is Mary's TechThis is Mary's TechThis is Mary's TechThis is Mary's Tech"
    )
)
'''

'''
#TC 7 Nick and Olga browse all available post in tech
print(
    get_posts(nick['access_token'], topic='tech'),
    get_posts(olga['access_token'], topic='tech')
)
'''


# TC8 Nick and Olga like Mary's post in the Tech topic
mary_post_id = 3
olga_post_id = 1
nick_post_id = 4

'''
print(like(nick['access_token'], post_id=mary_post_id))
print(get_post(nick['access_token'], post_id=mary_post_id))
print(like(olga['access_token'], post_id=mary_post_id))
print(get_post(olga['access_token'], post_id=mary_post_id))
'''

'''
# TC 9 Nestor likes Nick's post and dislikes Mary's post
print(like(nestor['access_token'], post_id=nick_post_id))
print(get_post(nestor['access_token'], post_id=nick_post_id))
print(dislike(nestor['access_token'], post_id=mary_post_id))
print(like(nestor['access_token'], post_id=mary_post_id))
'''

'''
# TC 10 Nick browses ll available posts in tech
print(get_posts(nick['access_token'], topic='tech'))
'''

'''
# TC 11 Mary likes her own post Should fail
print(like(mary['access_token'], mary_post_id))
'''

'''
# TC 12 Nick and Olga comment for Mary
print(
    comment(nick['access_token'], post_id=mary_post_id,
            message='Nick post for Mary')
)
print(
    comment(olga['access_token'], post_id=mary_post_id,
            message='Olga post for Mary')
)
'''

'''
# TC 13
print(get_posts(nick['access_token'], topic='tech'))
'''

'''
# TC 14 Nestor post a message to Health topic
print(
    create_post(
        token=nestor['access_token'], topic='health',
        title="This is Nestor's Health topic",
        duration=60,
        body="This is Nestor's TechThis is Nestor's TechThis is Nestor's TechThis is Nestor's Tech"
    )
)
'''
nestor_post_id = 5



'''
# TC 15
print(get_posts(mary['access_token'], topic='health'))
'''

'''
# TC 16 Mary comment on Nestor's post
print(
    comment(mary['access_token'], post_id=nestor_post_id,
            message='Mary comment for Nestor')
)
'''

'''
# TC 17 Mary dislikes Nestor's post in Health topic, should fail
print(dislike(mary['access_token'], nestor_post_id))
'''

'''
# TC 18
print(get_posts(nestor['access_token'], topic='health'))
'''

'''
# TC 19 should be empty
print(get_posts(nick['access_token'], topic='sport', status='expired'))
'''

'''
# TC 20 Nestor queries active post having the highest interest
print(get_posts(nestor['access_token'], topic='tech', status='active', activity='max'))
'''
