import dblp
import csv
import lxml
import time

pubs = {}
auth = {}

with open('people.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in reader:
		if row[0] not in auth:
			authors = dblp.search(row[0])
			print row[0] + ": " + str(len(authors)) + " author(s) found; " + str(len(authors[0].publications)) + " publications"
			
			for i in range(0, len(authors[0].publications)):
				year = authors[0].publications[i].year
				title = authors[0].publications[i].title
				
				if row[1] and year < row[1]:
					break
				if row[2] and year > row[2]:
					break
				
				if year not in pubs:
					pubs[year] = {}
					
				if title not in pubs[year]:
					pubs[year][title] = {}
					pubs[year][title]['year'] = authors[0].publications[i].year
					pubs[year][title]['authors'] = authors[0].publications[i].authors
					pubs[year][title]['journal'] = authors[0].publications[i].journal
					pubs[year][title]['date'] = authors[0].publications[i].mdate
					pubs[year][title]['booktitle'] = authors[0].publications[i].booktitle
					pubs[year][title]['url'] = authors[0].publications[i].ee
			
			auth[row[0]] = 1
			time.sleep(15)




for year in list(reversed(range(2000, 2016))):
	if year in pubs:
		for title in pubs[year]:
			pubs[year][title]["title"] = title


f = open("publications.html", "w")
for year in list(reversed(range(2000, 2016))):
	if year in pubs:
		f.write("\n<h3>" + str(year) + "</h3>\n\n")
		sorted_pubs = sorted(pubs[year].values(), key = itemgetter("date"), reverse = True)
		
		for i in range(0, len(sorted_pubs)):
			if len(sorted_pubs[i]["authors"]) > 0:
				f.write("<p>")
				f.write(', '.join(sorted_pubs[i]["authors"]).encode('utf-8').strip())
				f.write(". <a href='")
				if sorted_pubs[i]["url"] is not None:
					f.write(sorted_pubs[i]["url"])
				f.write("'><em>")
				f.write(sorted_pubs[i]["title"].encode('utf-8').strip())
				f.write("</em></a> ")
				if sorted_pubs[i]["booktitle"] is not None:
					f.write(sorted_pubs[i]["booktitle"].encode('utf-8').strip() + ". ")
				if sorted_pubs[i]["journal"] is not None:
					f.write(sorted_pubs[i]["journal"].encode('utf-8').strip() + " Journal. ")
			
				f.write(str(year) + ".</p>\n")

f.close()

