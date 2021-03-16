import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""

check_reddits = []
sum_reddits = []
app = Flask("DayEleven")

def sort_sum_reddits():
    reddit_len = len(sum_reddits) - 1
    for i in range(reddit_len):
        for j in range(reddit_len):
            index = sum_reddits[j]
            if(sum_reddits[j]['vote'] < sum_reddits[j + 1]['vote']):
                sum_reddits[j] = sum_reddits[j+1]
                sum_reddits[j+1] = index

def extract_pages(subreddits):
    sort_bool = 0
    for reddit in subreddits:
        if not reddit in check_reddits:
            sort_bool = 1
            check_reddits.append(reddit)
            url = f'https://www.reddit.com/r/{reddit}/top/?t=month'
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, "html.parser")
            postsector = soup.find('div', {'class': 'rpBJOHq2PR60pnwJlUyP0'})
            posts = postsector.find_all('div', {'class': '_1oQyIsiPHYt6nx7VOmd1sz'})
            for post in posts:
                check_promote = post.find('div', {"class": "_1poyrkZ7g36PawDueRza-J"}).find('span').string
                if check_promote == 'Posted by':
                    vote = post.find('div', {'class': '_1rZYMD_4xY3gRcSS3p8ODO'}).string
                    if not vote:
                        tempo_vote = post.find('div', {'class': '_1rZYMD_4xY3gRcSS3p8ODO'}).find('span', {'class': 'D6SuXeSnAAagG8dKAb4O4'}).string
                        vote = tempo_vote
                    if len(vote) > 3 and vote[3] == 'k':
                        vote = vote[0]+vote[2]+'00'
                    vote = int(vote)
                    title = post.find('h3', {'class': '_eYtD2XCVieq6emjKBH3m'}).string
                    link = post.find('a', {'class': 'SQnoC3ObvgnGjWt90zD9Z'})['href']
                    link = f'https://www.reddit.com{link}'
                    post_tempo_dict = {'vote': vote, "title": title, "link": link, "reddit": reddit}
                    sum_reddits.append(post_tempo_dict)
        else:
            print("do nothing")
    if(sort_bool == 1):
        sort_sum_reddits()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/read')
def read():
    subreddits = []
    words = request.args
    for word in words:
        subreddits.append(word)
    extract_pages(subreddits)
    last_sort_list = []
    for reddits in sum_reddits:
        if reddits['reddit'] in subreddits:
            last_sort_list.append(reddits)
    print(last_sort_list)
    return render_template('read.html', last_sort_list=last_sort_list, subreddits=subreddits)

app.run(host="0.0.0.0")