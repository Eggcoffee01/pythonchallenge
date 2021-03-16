import csv

def makecsv(term, data):
    f = open(f'{term}.csv', 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)
    wr.writerow(['Title', 'Company', 'Link'])
    for d in data:
        wr.writerow([d['title'], d['company'], d['link']])