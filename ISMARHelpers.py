

from ISMARTypes import *
from ISMARLoc import *




class ISMARHelpers:



    def  __init__(self):

        pass


    @staticmethod
    def DetermineAuthorCategory( author_db, paper_db):

        for last_names in author_db.keys():

            authors = author_db[last_names]

            for i in range(len(authors)):

                num_years_attendence = 0
                paper_in_year = dict()

                papers = authors[i].paper_list


                for p in papers:
                    year = paper_db[p].year
                    paper_in_year[year] = 1

                num_years_attendence = len(paper_in_year)

                if num_years_attendence > 15:
                    author_db[last_names][i].club_type = ISMARClubType.DIAMOND
                elif num_years_attendence >= 10:
                    author_db[last_names][i].club_type = ISMARClubType.GOLD
                elif num_years_attendence >= 5:
                    author_db[last_names][i].club_type = ISMARClubType.SILVER
                elif num_years_attendence >= 2:
                    author_db[last_names][i].club_type = ISMARClubType.BRONZE
                elif num_years_attendence == 1:
                    author_db[last_names][i].club_type = ISMARClubType.SINGLE_SHOT_AUTHOR

