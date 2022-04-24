import os
import praw
import datetime
import markdown

from dotenv import load_dotenv

load_dotenv()

client = praw.Reddit(
    client_id=os.getenv('ID'),
    client_secret=os.getenv('SECRET'),
    user_agent='testscript',
    username=os.getenv('NAME'),
    password=os.getenv('PASS'),
    redirect_uri='http://localhost:1111',
)

client.validate_on_submit = True

def sub(name):
    data = client.subreddit(name)
    setattr(data, 'subscribers', f'{data.subscribers:,}') # convert to comma-separated number
    setattr(data, 'name', data.display_name)
    setattr(data, 'type_char', 'r')
    
    return data

def user(name):
    data = client.redditor(name)
    setattr(data, 'subscribers', f'{data.comment_karma + data.link_karma:,} Karma') # convert to comma-separated number
    setattr(data, 'type_char', 'u')
    setattr(data, 'description', f'''
        {"🌟 Reddit Premium" if data.is_gold else ""}
        {"✅ Verified" if data.has_verified_email else ""}
        {"👮 Mod" if data.is_mod else ""}
        {"🔧 Reddit Employee" if data.is_employee else ""}
        {"🤝 Friends" if data.is_friend else ""}
    ''')

    return data

def posts(name, sort='hot', is_user=False): # fetch posts from subreddit
    if is_user:
        sub = client.redditor(name)
    else:
        sub = client.subreddit(name)
    
    posts = []

    fetch = sub.hot # default sort
    if sort == 'top': fetch = sub.top
    if sort == 'new': fetch = sub.new

    for p in fetch(limit=10):
        setattr(p, 'time', datetime.datetime.fromtimestamp(p.created_utc).strftime('%b %d %Y %H:%M')) # when the post was created
        
        if isinstance(p, praw.models.reddit.comment.Comment):
            setattr(p, 'text', p.body_html)
            setattr(p, 'url', p.permalink)
            setattr(p, 'subreddit', p.subreddit.display_name)
        else:
            setattr(p, 'text', markdown.markdown(p.selftext)) # convert markdown to HTML
        
        setattr(p, 'score', f'{p.score:,}')
        setattr(p, 'num_comments', f'{p.num_comments:,}')

        posts.append(p)

    return posts

def upvote(post):
    client.submission(post).upvote()

def downvote(post):
    client.submission(post).downvote()