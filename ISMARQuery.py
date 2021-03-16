

from ISMARTypes import ISMAREntry, ISMAR_DB, ISMARAuthor
from ISMARPlot import DataPlot
from ISMARLoc import *
from ISMARHelpers import *
from ISMARNetwork import *
import pickle
from collections import deque

class ISMARQuery:

    # global counter for authors
    author_id = 0

    db = None



    # dict with authors
    authors_db = {}

    # list of all author (id) and when they published at ismar
    authors_published_in = []

    # incorporates the number of connection between authors.
    paper_frequency = []


    network = 0


    def __init__(self, database = None):

        if(database != None):
            self.db = database
            self.__sort_authors__()
        else:
            self.db = ISMAR_DB()
            self.__read_from_file()


        # init the ismar network
        self.network = ISMARNetwork(self.authors_db, self.db)


    def __sort_authors__(self):
        """
        Go through all authors and assign ids to authors.
        Determine if authors are the same person of different persons.
        :return:
        """


        # Go through all publications and extract all authors.
        for e in self.db.db:

            # for each author
            for a in e.authors:

                found_author = False

                # find the last name in author db first.
                if a.last_name in self.authors_db:

                    # if the entry exits, compare the first names.
                    for i in range(len(self.authors_db[a.last_name])):
                        if a.first_name == self.authors_db[a.last_name][i].first_name:  # found author and entry.

                            self.authors_db[a.last_name][i].paper_list.append(e.myid)  ## add the paper to that author
                            self.authors_db[a.last_name][i].papers = self.authors_db[a.last_name][i].papers + 1
                            found_author  = True


                    #if found_author == False:
                    #    author = ISMARAuthor()
                    #    author.id = self.author_id
                    #    author.last_name = a.last_name
                    #    author.first_name = a.first_name
                    #    author.paper_list = list()
                    #    author.paper_list.append(e.id)
                    #    author.papers = 1

                    #    self.authors_db[a.last_name].append(author)
                    #    self.author_id = self.author_id + 1


                else:
                    self.authors_db[a.last_name] = list()

                if found_author == False:
                    author = ISMARAuthor()
                    author.id = self.author_id
                    author.last_name = a.last_name
                    author.first_name = a.first_name
                    author.paper_list = list()
                    author.paper_list.append(e.myid)
                    author.papers = 1

                    self.authors_db[a.last_name].append(author)
                    self.author_id = self.author_id + 1



        # Find all co-authors.
        for e in self.db.db:
            for a in e.authors:

                found_author = False

                # find the last name in author db first.
                if a.last_name in self.authors_db:

                    # if the entry exits, compare the first names.
                    for i in range(len(self.authors_db[a.last_name])):
                        if a.first_name == self.authors_db[a.last_name][i].first_name:  # found author and entry.

                            for co in e.authors:
                                if co.last_name == a.last_name and co.first_name == a.first_name:
                                    continue

                                if self.authors_db[a.last_name][i].coauthors == None:
                                    self.authors_db[a.last_name][i].coauthors = list()

                                coauthor = self.__getAuthor(co.first_name, co.last_name)

                                if coauthor == None:
                                    print("Could not find coauthor " + co.last_name + " for " + a.last_name )
                                    continue

                                self.authors_db[a.last_name][i].coauthors.append( (coauthor.id, e.myid) )


                            found_author = True

        # determine the author level
        ISMARHelpers.DetermineAuthorCategory(self.authors_db, self.db.db)

        self.__write_to_file()
        #self.__read_from_file()



   # print('Ready')

    def __getAuthor(self, first_name, last_name):

        matches = self.authors_db[last_name]

        for a in matches:
            if a.first_name == first_name:
                return a

        return None



    def __write_to_file(self):
        ismar_file = open('ismar.pickle', 'wb')

        data = {"paper" : self.db.db, "authors":self.authors_db, "autor_count":self.author_id}
        pickle.dump(data, ismar_file)
        ismar_file.close()


    def __read_from_file(self):

        ismar_file = open("ismar.pickle", "rb")
        data = pickle.load(ismar_file)

        self.db.db = data["paper"]
        self.authors_db = data["authors"]
        self.author_id = data["autor_count"]

        print("Loaded DB file\n")


    def __year2int(self, year):

        if year == 2002:
            return 0
        elif year == 2003:
            return 1
        elif year == 2004:
            return 2
        elif year == 2005:
            return 3
        elif year == 2006:
            return 4
        elif year == 2007:
            return 5
        elif year == 2008:
            return 6
        elif year == 2009:
            return 7
        elif year == 2010:
            return 8
        elif year == 2011:
            return 9
        elif year == 2012:
            return 10
        elif year == 2013:
            return 11
        elif year == 2014:
            return 12
        elif year == 2015:
            return 13
        elif year == 2016:
            return 14
        elif year == 2017:
            return 15
        elif year == 2018:
            return 16
        elif year == 2019:
            return 17
        elif year == 2020:
            return 18



    def AuthorFrequency(self):

        self.authors_published_in.clear()
        for i in range(self.author_id):
            self.authors_published_in.append(dict())



        # Count the number of publications and apperances per author
        for items in self.authors_db.items():


            for author in items[1]:

                for p in author.paper_list:

                    paper = self.db.db[ p]

                    if paper.year not in self.authors_published_in[author.id]:
                        self.authors_published_in[author.id][paper.year] = 0
                    self.authors_published_in[author.id][paper.year] =  self.authors_published_in[author.id][paper.year]  + 1




        y_15 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y_10 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        y_5 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        y_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        y_1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        years = ['2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']

        for item in self.authors_published_in:

            keys = item.keys()
            number = len(keys)

            # find all the authors that published more than 15 papers
            if number >= 15:

                for k in keys:
                    papers = item[k]
                    y_15[self.__year2int(k) ] = y_15[self.__year2int(k) ]  + 1

            elif number >= 10:

                for k in keys:
                    papers = item[k]
                    y_10[self.__year2int(k) ] = y_10[self.__year2int(k) ]  + 1

            elif number >= 5:

                for k in keys:
                    papers = item[k]
                    y_5[self.__year2int(k)] = y_5[self.__year2int(k)] + 1

            elif number >= 2:

                for k in keys:
                    papers = item[k]
                    y_2[self.__year2int(k)] = y_2[self.__year2int(k)] + 1

            elif number >= 1:

                for k in keys:
                    papers = item[k]
                    y_1[self.__year2int(k)] = y_1[self.__year2int(k)] + 1


        y_data = [y_1, y_2, y_5, y_10, y_15]
        labels = ["Single-shot-authors", "2-timers", "5-timers", "10-timers", "Evergreens"]
        title = "ISMAR Author Frequency"
        axis = ["Years", "Number of Authors" ]


        DataPlot.plotFrequency(years, y_data, labels, title, axis, "./out/author_frequence.png")



    def PaperFrequency(self):

        author_freq = []
        for i in range(self.author_id):
            author_freq.append(dict())


        ## Find the author frequency.
        ## The code counts how often an author appeared per year at ISMAR
        for items in self.authors_db.items():
            for author in items[1]:
                for p in author.paper_list:

                    paper = self.db.db[ p]

                    if paper.year not in author_freq[author.id]:
                        author_freq[author.id][paper.year] = 0
                    author_freq[author.id][paper.year] =  author_freq[author.id][paper.year]  + 1


        ## allocate some memory

        paper_scores = []
        self.paper_frequency.clear()
        for i in range( len(self.db.db)):
            self.paper_frequency.append(dict())



        ## calculate a paper score
        ## The paper score is
        ## a) the average score - (sum of := how is this author at ISMAR ) / num authors
        ## if = 1 -> all authors are for the first time at ISMAR>
        ## b) max score only counts the appearances of the most senior author = max apperances in 19 years ismar.
        for i in range(len(self.db.db)):

            paper = self.db.db[i]
            max_score = 0
            avg_score = 0
            for author in paper.authors:

                id = self.__getAuthorId(author.last_name, author.first_name)

                #score depends on the frequnce of authors apperances.
                entries =  author_freq[id]

                if len(entries) > max_score:
                    max_score = len(entries)

                for e in entries.values():
                    avg_score = avg_score + e

            avg_score = avg_score/ len(paper.authors)
            paper_scores.append((avg_score, max_score))



        y_25 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        y_15 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        y_10 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        y_5 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        y_1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        years = ['2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014',
                 '2015', '2016', '2017', '2018', '2019', '2020']

        # analyze the data
        for i in range(len(self.db.db)):

            if (paper_scores[i][1] >= 16):

                year = self.db.db[i].year

                y_25[self.__year2int(year)] = y_25[self.__year2int(year)] + 1

            elif (paper_scores[i][1] >= 10):

                year = self.db.db[i].year

                y_15[self.__year2int(year)] = y_15[self.__year2int(year)] + 1

            elif (paper_scores[i][1] >= 5):

                year = self.db.db[i].year

                y_10[self.__year2int(year)] = y_10[self.__year2int(year)] + 1

            elif (paper_scores[i][0] >= 2):

                year = self.db.db[i].year

                y_5[self.__year2int(year)] = y_5[self.__year2int(year)] + 1

            elif(paper_scores[i][0] == 1 ):
                # papers with author that appeared only once and never again.
                year = self.db.db[i].year

                y_1[self.__year2int(year)] =  y_1[self.__year2int(year)]  + 1


        y_data = [y_1, y_5, y_10, y_15, y_25]
        labels = ["Single-shot-authors", "2-4 apperances", "5-9 apperances", "10-15 apperances", "Evergreens"]
        title = "ISMAR Paper/Poster Most Senior Author"
        axis = ["Years", "Number of Papers"]

        DataPlot.plotFrequency(years, y_data, labels, title, axis, "./out/paper_frequence.png")





    def __getAuthorId(self, last_name, first_name):
        if last_name not in self.authors_db:
            print("Author " + last_name + " not in db")
            return -1

        authors = self.authors_db[last_name]

        for aa in authors:
            if aa.first_name == first_name:
                return aa.id



    def FindAuthor(self, last_name):

        if last_name not in self.authors_db:
            print("Author " + last_name + " not in db")
            return

        authors = self.authors_db[last_name]

        if(len(authors) > 1):
            print("\nAuthor with the name " + last_name + " appears " + str(len(authors)) + " times" )


        for aa in authors:
            paper_list = []



            for p in aa.paper_list:
                paper = self.db.db[p]
                paper_list.append((paper.year,p))

            print("\nPapers for author " + aa.first_name + " " + last_name + " (" + str(len(paper_list))  + " appearances)")
            print("ISMAR status: " + ISMARClubType.to_str(aa.club_type) + "\n")
            # sort
            paper_list.sort(key=lambda x: x[0], reverse=True)

            for p in paper_list:
                self.__print_paper(p[1])

            #print("The author appers " + str(len(paper_list)) + " times")

            self.CalculateBillinghurstDistance(aa.last_name, aa.first_name)

            print("---------------------------------------------------------------------------\n")



    def PublicationStatusStatistics(self):
        """
        Print a table that shows the number of papers for each category (SSA, Bronze, Silver, Gold, Diamond) for
        each year of ISMAR.
        :return:
        """

        years = ISMARYears.list()

        status_labels = ISMARClubType.list()

        all_years_data = dict()

        # Get the data for all years
        for year in years:
            all_years_data[year] =  self.PublicationsForYear( year, with_author_seniority=True)


        # print a table
        print("\nStatistics for all years")

        row = "Year\t"
        for l in status_labels:
            row += l
            row += "\t"
        print(row)
        print("--------------------------------------------------------------------")


        years.reverse()

        for year in years:
            row = str(year) + "\t"
            data = all_years_data[year]

            for l in status_labels:
                num = 0
                if l in data:
                    num = data[l]
                row += str(num)
                row += "\t\t"
            print(row)



    def PublicationsForYear(self, query_year, with_author_seniority = False):

        print("All papers (journal, paper, poster) for ISMAR " + str(query_year) + "\n")

        seniority_statistics = dict()

        count = 0

        for paper in self.db.db:

            if paper.year == query_year:

                # find seniority of this paper
                if with_author_seniority == True:
                    author_max_senority = ISMARClubType.SINGLE_SHOT_AUTHOR
                    for author in paper.authors:

                        a = self.__getAuthor(author.first_name, author.last_name)

                        if a.club_type.value > author_max_senority.value:
                            author_max_senority = a.club_type

                    print("Status: " + author_max_senority.name)

                    if author_max_senority.name not in seniority_statistics:
                        seniority_statistics[author_max_senority.name] = 0

                    seniority_statistics[author_max_senority.name] = seniority_statistics[author_max_senority.name] + 1


                # print the paper
                self.__print_paper(paper.myid)
                count = count+1

        print("Total: " + str(count))
        if with_author_seniority == False:
            return



        print("\nAuthor Status per Paper\nStatus\t\t\tNum papers")

        status_labels = ISMARClubType.list()

        for label in status_labels:

            status = 0
            if label in seniority_statistics:
                status = seniority_statistics[label]

            if label == "SINGLE_SHOT_AUTHOR":
                print(label + "\t" + str(status))
            else:
                print(label + "\t\t\t\t" + str(status))

        return seniority_statistics


    def PublicationClubStatus(self):

        years = ISMARYears.list()


        # Determine the statistics for all years
        seniority_statistics = dict()

        for year in years:

            seniority_statistics_per_year = dict()

            for paper in self.db.db:

                if paper.year == year:

                    # find seniority of this paper
                    author_max_senority = ISMARClubType.SINGLE_SHOT_AUTHOR

                    for author in paper.authors:

                        a = self.__getAuthor(author.first_name, author.last_name)

                        if a.club_type.value > author_max_senority.value:
                            author_max_senority = a.club_type


                    if author_max_senority.name not in seniority_statistics_per_year:
                        seniority_statistics_per_year[author_max_senority.name] = 0

                    seniority_statistics_per_year[author_max_senority.name] = seniority_statistics_per_year[
                                                                         author_max_senority.name] + 1


            seniority_statistics[year] = seniority_statistics_per_year


        # Convert to plot data
        status_y = list()

        for i in range(ISMARClubType.size()):
            status_y.append(list())

        # status_y[0] -> Diamond
        # status_y[4] - Single shot author

        status_labels = ISMARClubType.list()

        status_labels = [ele for ele in reversed(status_labels)]

        for year in years:

            for i in range(ISMARClubType.size()):

                data = seniority_statistics[year]
                status_label = status_labels[i]

                num = 0
                if status_label in data:
                    num = data[status_label]

                status_y[i].append(num)


        DataPlot.plotFrequency( ISMARYears.string(), status_y, status_labels , "Most Senior Author Status",  ["Years", "Num papers"], "./out/paper_status.png")
        DataPlot.plotStackNormalized(ISMARYears.string(), status_y, ["SSA", "Bronze",  "Silver",  "Gold", "Diamond"], "ISMAR Paper Status Develoopment",
                               ["Years", "Percentage Contributions / Year"], "./out/paper_status_stack.png")





    def __print_paper(self, paper_id):

        paper = self.db.db[paper_id]

        author_str = ""
        c = 0
        for a in paper.authors:
            if c > 0:
                author_str += (" and ")
            author_str+= (a.first_name + " " + a.last_name)
            c = c + 1

        author_str += ", "
        author_str += str(paper.year)
        author_str += ", "
        print(author_str)
        print(paper.title)
        author_str += ", "
        if paper.is_TVCG ==  False:
            print(paper.data['booktitle'])
        else:
            volume = ", "
            if 'volume' in paper.data:
                volume = paper.data['volume']
            if 'number' in paper.data:
                volume = volume + ":" + paper.data['number']

            print(paper.data['journal'] + " " +volume + " (TVCG)")
        print("\n")



    def __determine_paper_status(self, paper_id):
        """
        Determine the status of a paper (SSA, Bronze, Silver, Gold, Diamond).
        The status of the paper is equal to the maximum seniority level (SSA, Bronze, Silver, Gold, Diamond)
        of its most senior author.
        :param paper_id: the paper myid id as integer.
        :return: the seniority status as ISMARClubType
        """

        paper = self.__getPaperById(paper_id)


        author_max_senority = ISMARClubType.SINGLE_SHOT_AUTHOR
        for author in paper.authors:

            a = self.__getAuthor(author.first_name, author.last_name)

            if a.club_type.value > author_max_senority.value:
                author_max_senority = a.club_type

        return author_max_senority



    def PrintYear(self, query_year):

        count = 0
        authors_numbers = 0
        for paper in self.db.db:

            if paper.year == query_year:
                self.__print_paper(paper.myid)
                authors_numbers = authors_numbers + len(paper.authors)  # invalid, authors may be count twice
                count = count+1

        # count the authors. This makes sure that every author is only count once.
        author_count = 0
        for authors in self.authors_db.values():
            for aa in authors:
                for paper_id in aa.paper_list:
                    y = self.db.db[paper_id].year

                    if y == query_year:
                        author_count = author_count + 1
                        break # we only need to count one.




        print("ISMAR " + str(query_year) + " had " + str(count) + " contributions from " + str(author_count) + " authors (" + str(authors_numbers)+ " with double count)."  )



    def PrintKeywords(self, query_year, num = 30):

        ## keyword / count
        keywords = dict()

        for paper in self.db.db:

            if paper.year == query_year:
                kw = paper.data["keywords"].split(';')
                for word in kw:
                    if word.lower() not in keywords:
                        keywords[word.lower()] = 1
                    else:
                        keywords[word.lower()] = keywords[word.lower()] + 1

        sorted = list()
        for a in keywords.keys():

            count = keywords[a]
            sorted.append((a, count))

        # sort
        sorted.sort(key=lambda x: x[1], reverse=True)

        print("\nFound " + str(len(sorted)) + " different keywords")

        for i in range(num):
            print(str(sorted[i][0]) + " - " + str(sorted[i][1])  )


    def FirstAuthorFrequency(self):


        first_author_freq = []
        for i in range(self.author_id):
            first_author_freq.append(dict())


        ## Find the author frequency.
        ## The code counts how often an author appeared per year at ISMAR
        for items in self.authors_db.items():
            for author in items[1]:
                for p in author.paper_list:

                    paper = self.db.db[p]

                    # check if the author is the first author of this paper
                    if paper.first_author_first == author.first_name and paper.first_author_last == author.last_name:

                        if paper.year not in first_author_freq[author.id]:
                            first_author_freq[author.id][paper.year] = 0
                        first_author_freq[author.id][paper.year] = first_author_freq[author.id][paper.year] + 1


        print('readfty')

        y_15 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        y_10 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        y_5 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        y_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        y_1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        year_labels = ['2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014',
                 '2015', '2016', '2017', '2018', '2019', '2020']


        for a in first_author_freq:

            years = a.keys()
            num_years = len(years)


            if num_years >= 15:

                for k in years:
                    papers = a[k]
                    y_15[self.__year2int(k) ] = y_15[self.__year2int(k) ]  + 1

            elif num_years >= 10:

                for k in years:
                    papers = a[k]
                    y_10[self.__year2int(k) ] = y_10[self.__year2int(k) ]  + 1

            elif num_years >= 5:

                for k in years:
                    papers = a[k]
                    y_5[self.__year2int(k)] = y_5[self.__year2int(k)] + 1

            elif num_years >= 2:

                for k in years:
                    papers = a[k]
                    y_2[self.__year2int(k)] = y_2[self.__year2int(k)] + 1

            elif num_years == 1:

                for k in years:
                    papers = a[k]
                    y_1[self.__year2int(k)] = y_1[self.__year2int(k)] + 1


        y_data = [y_1, y_2, y_5, y_10, y_15]
        labels = ["Single-shot-authors", "2-4 apperances", "5-9 apperances", "10-15 apperances", "Evergreens"]
        title = "ISMAR Paper/Poster First Author"
        axis = ["Years", "Number of Papers"]

        DataPlot.plotFrequency(year_labels, y_data, labels, title, axis, "./out/paper_first_author_frequence.png")



    def AverageAuthorsPerPaper(self):


        papers_per_author = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        papers_per_author_max = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        authors_per_year = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        authors_per_paper = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        author_count = 0

        # save all the published numbers of articles for every author per year
        all_number_pre_year = dict()

        for authors in self.authors_db.values():

            for author in authors:

                # determine in what years an indvidual author published
                years_published =  {}
                for paper_id in author.paper_list:

                    paper = self.db.db[paper_id]

                    year_id = self.__year2int(paper.year)
                    if paper.year not in years_published:
                        years_published[paper.year] = 0
                    years_published[paper.year] = years_published[paper.year] + 1

                    # numbers of paper published in this year
                    papers_per_author[year_id] = papers_per_author[year_id] + 1



                ## count every author once regardless of the number of publications
                for y in years_published.keys():
                    authors_per_year[self.__year2int(y)] = authors_per_year[self.__year2int(y)]  + 1


                    # preseve all paper counts of thsi author for this year
                    if y not in all_number_pre_year:
                        all_number_pre_year[y] = list()

                    all_number_pre_year[y].append(years_published[y])


                # determine the maximum numbner of publications an author had per year
                for y in years_published.keys():
                    y_id = self.__year2int(y)

                    value = years_published[y]

                    if value > papers_per_author_max[y_id]:
                        papers_per_author_max[y_id] = value



        for i in range(len(papers_per_author)):
            papers_per_author[i] = papers_per_author[i] / authors_per_year[i]

        median_authors_per_paper = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # find the median per year
        for year in all_number_pre_year.keys():

            numbers = all_number_pre_year[year]
            numbers.sort(key=lambda x: x, reverse=True)

            count = len(numbers)
            id = int(count/2)
            median = numbers[id]

            median_authors_per_paper[self.__year2int(year)] = median



        #plot

        year_labels = ['2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013',
                       '2014',
                       '2015', '2016', '2017', '2018', '2019', '2020']

        y_data = [papers_per_author, papers_per_author_max, median_authors_per_paper]
        labels = ["Avg. papers per author", "Max papers of an author", "Median papers per author"]
        title = "ISMAR Paper/Poster Papers published per Author"
        axis = ["Years", "Number of Papers"]

        DataPlot.plotFrequency(year_labels, y_data, labels, title, axis, "./out/papers_pre_author.png")



        print('ready')


    def AllAuthorNetworks(self, plot = False, with_BD= False):

        years = [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]

        for year in years:
            print("Preparing " + str(year))
            self.AuthorNetwork(year, plot)





    def AuthorNetwork(self, query_year, plot = False, with_BD = False):


        # Go through all authors and look for all co-authors in a particular year.
        # connections[i][j]    connection from to. id and j are author ids
        connections = dict()

        author_count = 0
        distance = 0

        for authors in self.authors_db.values():

            for author in authors:

                for paper_id in author.paper_list:

                    if self.db.db[paper_id].year == query_year:

                        paper = self.db.db[paper_id]

                        author_id = author.id

                        author_count = author_count + 1

                        if author_id not in connections:
                            connections[author_id] = list()


                        if with_BD == True:
                            dist, path = self.network.CalculateBillinghurstDistance(author.last_name, author.first_name)
                            distance = distance  + dist

                        for coauthor in paper.authors:


                            co_id = self.__getAuthorId(coauthor.last_name, coauthor.first_name)
                            if co_id == author_id:
                                continue


                            #if author_id not in connections:
                            #    connections[author_id] = list()

                            connections[author_id].append(co_id)

                       # if len(connections[author_id]) == 0:
                       #     print("no coauthor: " + str(author_id))


        # create a weighted graph

        weighted_graph = dict()
        num_nodes = 0

        for node in connections.keys():

            if node ==3165:
                c = connections[node]

            if len(connections[node]) == 0:
                weighted_graph[node] = dict()


            for edge in connections[node]:

                if node not in weighted_graph:
                    weighted_graph[node] = dict()

                if edge not in weighted_graph[node]:
                    weighted_graph[node][edge] = 0


                weighted_graph[node][edge] = weighted_graph[node][edge] + 1



        # plot
        if plot == True:
            DataPlot.plotGraph(weighted_graph)




        # Search for connected components / topological search

        visited = list()
        num_groups = 0
        groups = list()

        queue = deque()

        while len(visited) < len(weighted_graph):

            # for all nodes
            for from_node in weighted_graph.keys():

                if from_node not in visited:
                    queue.append(from_node)
                    groups.append(list())
                    num_groups = num_groups + 1


                # breath first search
                while len(queue) > 0:

                    current_node = queue.popleft()
                    visited.append(current_node)
                    groups[num_groups - 1].append(current_node)

                    for child in weighted_graph[current_node].keys():

                        if child in visited or child in queue:
                            continue

                        queue.append(child)


        # determine for how much papers each group is repsonsible

        papers_per_group = list()  # counts the papers per group.
        papers_title_per_group = list()  # remembers the paper tiles (ids per group). It is a dict with (id, count).

        for i in range(len(groups)):

            members = groups[i]
            paper_ids_per_group = dict()   # paper id and count. It is a dict to prevent double counts, the keys are the titles

            for m in members:  # m is the author id

                author = self.__getAuthorById(m)
                papers_author = author.paper_list

                for paper in papers_author: # paper is the paper myid

                    if self.db.db[paper].year != query_year:
                        continue

                    if paper not in paper_ids_per_group:
                        paper_ids_per_group[paper] = 0
                    paper_ids_per_group[paper] = paper_ids_per_group[paper] + 1

            papers_per_group.append(len(paper_ids_per_group))
            papers_title_per_group.append(paper_ids_per_group)



        # statistics number of groups. Group is defined by the number of paper published.

        statistics = dict()
        statistics_pers_all_groups = dict()

        num_all_contributions = 0

        for i in range(len(groups)):

            members = groups[i]


            num_members = len(members)
            num_papers =  papers_per_group[i]


            if num_papers not in statistics:
                statistics[num_papers] = 0
                statistics_pers_all_groups[num_papers] = 0

            statistics[num_papers] = statistics[num_papers] + 1  # count the group of single paper, two paper, etc. groups
            statistics_pers_all_groups[num_papers] = statistics_pers_all_groups[num_papers] + num_papers

            num_all_contributions = num_all_contributions + num_papers


        #---------------------------------------------------------------------
        # for all groups-statistics, determine how many papers they have per status.

        status_statistics = dict()

        for i in range(len(groups)):

            members = groups[i]
            num_papers = papers_per_group[i]

            for paper_id in papers_title_per_group[i].keys():

                status = self.__determine_paper_status(paper_id)

                if num_papers not in status_statistics:
                    status_statistics[num_papers] = dict()

                if status not in status_statistics[num_papers]:
                    status_statistics[num_papers][status] = 0

                status_statistics[num_papers][status] = status_statistics[num_papers][status] + 1



        # Billinghurst distance
        distance = float(distance) / float(author_count)




        #---------------------------------------------------------------------
        # Sort all keys

        # get a sorted list of keys
        keys_sorted = []
        for k in statistics.keys():
            keys_sorted.append(k)
        keys_sorted.sort()

        # ---------------------------------------------------------------------
        # Get some statistics

        # contribution of each status group.
        status_labels_enum = ISMARClubType.enum_sorted()
        percentage_dict = dict()
        for k in status_labels_enum:
            value = 0
            for s in keys_sorted:

                data = status_statistics[s]

                if k in data:
                    value = value + data[k]

            percentage_dict[k] = value


        # contribution of each size group
        percentage_group_dict = dict()
        sum = 0
        for s in keys_sorted:
            value = 0
            for k in status_labels_enum:


                data = status_statistics[s]

                if k in data:
                    value = value + data[k]

            percentage_group_dict[s] = value
            sum = sum + value

        for k in percentage_group_dict.keys():
            percentage_group_dict[k] = float(percentage_group_dict[k]) / float(sum)


        # ---------------------------------------------------------------------
        # write results to a file

        filename = "./out/ISMAR_Network_" + str(query_year) + ".txt"

        title = "ISMAR Network " + str(query_year) + "\n" +  ISMARLoc.yearToString(query_year) +  "\n\n"

        f = open(filename, "w")
        f.write(title)


        f.write("Number of Groups: " + str(len(groups)) + "\n")

        for i in range(len(groups)):

            num_members = len(groups[i])
            num_papers = papers_per_group[i]

            f.write("Group #" + str(i) + "\tmembers: " + str(num_members) + "\tpapers: " + str(num_papers) + "\n")

        f.write("\n\nStatistics\n")
        f.write("Groups are ordered with respect to the number of papers published\n")
        f.write("\t\t\tNum groups\tNum paper/poster\tpercentage\n")

        for s in keys_sorted:

            out = "papers/group\t" + str(s) + "\t" + str(statistics[s] ) + "\t\t" + str(statistics_pers_all_groups[s]) + "\t\t" + str(float(statistics_pers_all_groups[s]) /float(num_all_contributions))[0:5] + "\n"
            f.write(out)



        #  -- print the club statistics
        f.write("\n")
        f.write("\n\nStatus statistics\n\t\t\t")

        status_labels = ISMARClubType.list()


        out = ""
        for l in status_labels:
            out += l
            out += "\t"

        out += "%"

        f.write(out +"\n")

        out = ""
        for s in keys_sorted:
            out = "papers/group\t" + str(s) + "\t"

            data = status_statistics[s]

            status_labels_enum = ISMARClubType.enum_sorted()

            for k in status_labels_enum:
                num = 0
                if k in data:
                    num = data[k]
                out += str(num)
                out += "\t"

            p = percentage_group_dict[s]
            out+= str(p)[0:5]

            f.write(out + "\n")





        # p -- print the percentage statistics.
        out = "percentage\t\t"
        for v in status_labels_enum:

            out += str(float(percentage_dict[v])/float(num_all_contributions))[0:5]
            out += "\t"

        f.write(out)

        f.write("\n\n")

        if with_BD == True:
            f.write("Billinghurst-Distance " + str(distance))
            f.write("\n\n")

        for i in range(len(groups)):

            f.write("\n----------------------------------------------------------- \n")
            f.write("Group #"+ str(i) + "\n")
            f.write("Papers: " + str(papers_per_group[i]) + "\n" )
            f.write("\nMembers \n")

            members = groups[i]

            for m in members: # m is member id

                author = self.__getAuthorById(m)

                f.write(author.first_name + " " + author.last_name + "\n")


            f.write("\n")

            papers = papers_title_per_group[i]

            for paper_id in papers: # paper is paper id


                paper_status = self.__determine_paper_status(paper_id)
                f.write("Paper status: " + ISMARClubType.to_str(paper_status) + "\n")
                paper = self.__getPaperById(paper_id)
                names = ""
                for author in paper.authors:

                    names += author.first_name
                    names += " "
                    names += author.last_name
                    names += ", "

                names += str(paper.year)
                names += '\n'
                f.write(names)

                f.write(paper.title)
                f.write("\n")
                f.write(paper.data["booktitle"])
                f.write("\n\n")


        f.close()



        print("ready")






    def __getAuthorById(self, id):

        # exhaustive search. That can go better

        for authors in self.authors_db.values():

            for author in authors:

                if author.id == id:
                    return author



    def __getPaperById(self, id):

        return self.db.db[id]



    def CalculateBillinghurstDistance(self, last_name, first_name, output=True):

        mb_distance, walked_path =  self.network.CalculateBillinghurstDistance(last_name, first_name)

        if output == False:
            return

        print( "Billinghurst-distance: " + str(mb_distance))

        if len(walked_path) == 0:
            print("No path found")
            return


        first = walked_path[0]
        author = self.__getAuthorById(first)

        out = "Path: " + author.last_name

        for i in range(len(walked_path) - 1):
            id = walked_path[i+1]
            author = self.__getAuthorById(id)
            out += " -> "
            out += author.last_name

        print(out)


