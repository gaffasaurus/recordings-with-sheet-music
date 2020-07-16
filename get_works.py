import json
import requests
import sys
import unidecode

works = {}

composers = []

def remove_accent(name):
    return unidecode.unidecode(name)

def get_composers():
    file = open('composers.txt', 'r')
    lines = file.readlines()
    for line in lines:
        # unaccent = unidecode.unidecode(line.strip())
        composers.append(line.strip())

get_composers()

# def sort_composers():
#     new_file = open('composers2.txt', 'w')
#     old_file = open('composers.txt', 'r')
#     lines = old_file.readlines()
#     for line in lines:
#         names = line.split()
#         formatted = remove_accent(names[-1] + ", " + " ".join(names[:-1]) + '\n')
#         composers.append(formatted)
#     composers.sort()
#     for composer in composers:
#         new_file.write(composer)
#
# sort_composers()

def parse_works():
    url = ""
    for i in range(164):
        counter = i * 1000
        url = "https://imslp.org/imslpscripts/API.ISCR.php?account=worklist/disclaimer=accepted/sort=id/type=2/start=" + str(counter) + "/retformat=json"
        r = requests.get(url)
        data = r.json()
        for i in range(len(data) - 1):
            work_info = data[str(i)]['intvals']
            composer = remove_accent(work_info['composer'])
            if composer not in composers:  # Only add listed composers
                continue
            # title = remove_accent(work_info['worktitle'])
            url = data[str(i)]['permlink']
            if works.get(composer) == None:
                works[composer] = [url]
            else:
                works[composer].append(url)
    return works

def write_JSON():
    with open("works.json", "w") as outfile:
        json.dump(parse_works(), outfile)

def read_JSON():
    with open("works.json") as json_file:
        try:
            data = json.load(json_file)
        except:
            return "empty"
        return data

write_JSON()
works = read_JSON()
length = 0
for key in works:
    length += len(works[key])
print(length)
