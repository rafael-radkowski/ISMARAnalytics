
import bibtexparser
from ISMARTypes import ISMAREntry, ISMAR_DB, ISMARAuthor
import os


global_id_counter = 0

def parse_name(name_str, names):


    l = len(name_str)

    line = name_str

    while l > 0:

        author = ISMARAuthor()

        idx0 = line.rfind('}')
        idx1 = line.rfind('{')

        name = line[idx1+1:idx0]

        idx2 = line.rfind("and")

        first = ""
        if idx2 > -1:
            first = line[idx2+4: idx1-1]
        else:
            first = line[0: idx1 - 1]
            idx2 = 0
            first_author = True

        author.last_name = name.strip()
        author.first_name = first.replace(" ", "") # remove all white space

        names.append(author)

        line = line[0:idx2]

        l = len(line)



def bib2Item(bibtex_database, ISMAR_DB):
    global global_id_counter
    c = 0

    for b in bibtex_database.entries_dict.items():

        item = ISMAREntry()

        valid_item = False



        if b[1]['ENTRYTYPE'].lower() == "inproceedings" or b[1]['ENTRYTYPE'] == "article":
            valid_item = True

        if valid_item == False:
            continue

        if 'author' not in b[1]:
            continue

        if len( b[1]['author']) == 0:
            continue


        if b[1]['ENTRYTYPE'] == "article":
            item.is_TVCG = True
        else:
            item.is_TVCG = False



        item.id = b[0]
        item.title = b[1]['title']
        item.year = int(b[1]['year'])

        item.data = dict()
        item.data['month'] = ""
        item.data['doi'] = ""
        item.data['keywords'] = ""
        item.data['abstract'] = ""
        item.data['number'] = ""
        item.data['volume'] = ""
        item.data['booktitle'] = ""
        item.data['journal'] = ""
        item.data['author'] = ""

        if 'month' in b[1]:
            item.data['month'] = b[1]['month']

       # item.data['issn'] = b[1]['issn']
        if 'doi' in b[1]:
            item.data['doi'] = b[1]['doi']

        if 'keywords' in b[1]:
            item.data['keywords'] = b[1]['keywords']

        if 'abstract' in b[1]:
            item.data['abstract'] = b[1]['abstract']

        item.data['pages'] = b[1]['pages']

        if 'number' in b[1]:
            item.data['number'] = b[1]['number']

        if 'volume' in b[1]:
            item.data['volume'] = b[1]['volume']

        item.data['year'] = b[1]['year']
        item.data['title'] = b[1]['title']

        if 'booktitle' in b[1]:
            item.data['booktitle'] = b[1]['booktitle']

        if 'journal' in b[1]:
            item.data['journal'] = b[1]['journal']

        item.data['author'] = b[1]['author']

        item.authors = list()
        parse_name(b[1]['author'],  item.authors)

        item.myid = global_id_counter
        global_id_counter = global_id_counter + 1


        item.first_author_first = item.authors[0].first_name
        item.first_author_last = item.authors[0].last_name


        ISMAR_DB.db.append(item)

        c = c+1

    print("Added " + str(c) + " items.")


def LoadBibTex(path, db):

    bibfiles = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".bib"):
                p = os.path.join(root, file)
                #print(p)
                bibfiles.append(p)


    for file in bibfiles:

        bibtex_file =  open(file)
        bib_database = bibtexparser.load(bibtex_file)

        print("Parsing " + file)

        bib2Item(bib_database, db)

    print("Loaded " + str(len(db.db)) + " items")