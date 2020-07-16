import requests
import bs4 as bs
from bs4 import BeautifulSoup
import time
import json
import sys

def read_JSON():
    with open("works.json") as json_file:
        try:
            data = json.load(json_file)
        except:
            return "empty"
        return data

works = read_JSON()
scores = {}

program_start = time.time()

for composer in works:  #Get works pages
    for url in works[composer]:
        info = {'title': "", 'catalogue': "", 'search_tags': [], 'score': ""}  #Search tags are used when searching for this work

        start_time = time.time()
        r = requests.get(url)

        soup = BeautifulSoup(r.content, 'html.parser')

        #Get title of work
        heading = soup.find(class_="firstHeading pagetitle page-header").get_text().split('(')[0].strip().lower() # Gets title from heading
        info['title'] = heading

        #Add title and alternate titles to search tags
        title_html = soup.find(class_="wi_body")
        if title_html != None:
            titles = soup.find(class_="wi_body").find_all("td", class_="wi_head")
            for title in titles:
                info['search_tags'].append(title.get_text().strip().lower())
        else:   # Probably means the page is empty/redirects, this will prevent error
            continue


        #Get info from table at bottom of page
        info_table = soup.find(class_="wi_body")

        #Get movements/sections
        table_rows = info_table.find_all(class_="mh555")
        sections = "empty"
        for row in table_rows:
            if row.get_text() == "Movements/Sections":
                main_row = row.parent.parent
                if len(main_row.find_all("i")) > 1:
                    sections = main_row.find_all("i")
                elif len(main_row.find_all("li")) > 1:
                    sections = main_row.find_all("li")
                elif len(main_row.find_all("td")) > 1:
                    sections = main_row.find_all("td")
                elif len(main_row.find_all("dd")) > 1:
                    sections = main_row.find_all("dd")
                break;
        if sections != "empty":
            for section in sections:
                info['search_tags'].append(section.get_text().strip().lower().replace(u'\xa0', " ").replace('♭', 'b'))

        #Get key of piece
        rows = info_table.find_all('tr')
        for row in rows:
            th = row.find('th')
            if th != None and th.get_text() == "Key":
                key_row = row.parent
                info['search_tags'].append(key_row.find('td').get_text().lower())
                break

        #Get opus/catalogue number
        opus_num = "empty"
        for row in table_rows:
            if row.get_text() == "Opus/Catalogue Number":
                main_row = row.parent.parent
                td = main_row.find('td')
                if td != None:
                    info['catalogue'] = (td.get_text())
                    break

        #Get info about scores and pick the best one
        scores_list = []
        def get_downloads(score):
            loc = score.find(class_="we_file_info2").find('span', {'class': "uctagonly mh900"}).next_sibling.next_sibling
            try:
                downloads = loc.find('a').get_text()
            except:
                downloads = loc.get_text()
            try:
                int(downloads)
            except:
                downloads = -1
            return downloads

        def get_url(score):
            return score.find(class_="external text")['href']

        def get_name(score):
            return score.find(title="Download this file").get_text()

        has_scores = True
        try:
            scores_html = soup.find(id="wpscore_tabs").find(id="tabScore1").find_all(class_="we")
        except:
            try:
                scores_html = soup.find(id="wpscore_tabs").find(id="tabArrTrans").find_all(class_="we")
            except:
                has_scores = False

        def get_score_info():
            for score in scores_html:
                for child_score in score.children:
                    if child_score.name == "div":
                        try:
                            downloads = int(get_downloads(child_score))
                        except:
                            downloads = -1
                        try:
                            url = get_url(child_score)
                        except:
                            url = ""
                        try:
                            name = get_name(child_score).lower().strip()
                        except:
                            name = ""
                        if url != "" and "complete" in name:
                            scores_list.append((url, downloads, name))
        if has_scores:  # If Scores and Arrangements/Transcriptions tabs are both missing, skip this, 'score' will be set to "none" by choose_score()
            get_score_info()

        def choose_score():
            downloads = []
            for score in scores_list:
                downloads.append(score[1])
            if len(downloads) == 0:
                return "none"
            else:
                ix_max = downloads.index(max(downloads))
                return scores_list[ix_max][0]

        info['score'] = choose_score()

        end_time = time.time() - start_time

        if scores.get(composer) == None:
            scores[composer] = [info]
        else:
            scores[composer].append(info)
        sys.stdout.flush()
        sys.stdout.write('\r')
        sys.stdout.write(composer + ": " + str(len(scores[composer])) + " out of " + str(len(works[composer])))
        if end_time < 2:
            time.sleep(2 - end_time)

    #Remove any duplicates
    hashable = []
    for work in scores[composer]:
        hashable.append(json.dumps(work, sort_keys=True))
    dicts_set = set(hashable)
    scores_no_dupes = []
    for dict in dicts_set:
        scores_no_dupes.append(json.loads(dict))
    scores[composer] = scores_no_dupes
    #See progress
    print("\nProgress: " + str(len(scores)) + "/" + str(len(works)))

#Write to JSON
def write_JSON():
    with open("scores.json", "w") as outfile:
        json.dump(scores, outfile)
write_JSON()

runtime = time.time() - program_start
print("\nExecution time: " + str(runtime))
