"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""
from flask import Flask, render_template, request, send_file
from scrapper import scrapper_handler
from make_csv import makecsv

db = {}

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search')
def search():
    term = request.args.get('term')
    term = term.lower()
    if term in db:
        print(1)
    else:
        term_data = scrapper_handler(term)
        db[term] = term_data
        makecsv(term, db[term])
    return render_template('search.html', database=db[term], len=len(db[term]), term=term)

@app.route('/<term>')
def asd(term):
    print(term)
    return send_file(f'{term}.csv', as_attachment=True)


app.run()