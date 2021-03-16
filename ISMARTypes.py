


from enum import Enum


class ISMARYears:


    @staticmethod
    def list():
        return [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]


    @staticmethod
    def string():
        return ['2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014',
                 '2015', '2016', '2017', '2018', '2019', '2020']




class ISMARClubType(Enum):
    """
    The category indicates how often the author attendend
    the ISMAR conference.
    """

    DIAMOND = 5  # authors with more than 16 attendences
    GOLD = 4     # authors with 10-15 attendences
    SILVER = 3   # authors with 5-9 attendences
    BRONZE = 2   # authors with 2-4 attendences
    SINGLE_SHOT_AUTHOR = 1   # authors with one attendence only

    @staticmethod
    def to_str(type ):

        if type == ISMARClubType.DIAMOND:
            return "Diamond"
        elif type == ISMARClubType.GOLD:
            return "Gold"
        elif type == ISMARClubType.SILVER:
            return "Silver"
        elif type == ISMARClubType.BRONZE:
            return "Bronze"
        elif type == ISMARClubType.SINGLE_SHOT_AUTHOR:
            return "Single-Shot Author"

    @staticmethod
    def list():
        return ["DIAMOND", "GOLD", "SILVER", "BRONZE", "SINGLE_SHOT_AUTHOR" ]

    @staticmethod
    def enum_sorted():
        return [ISMARClubType.DIAMOND, ISMARClubType.GOLD, ISMARClubType.SILVER, ISMARClubType.BRONZE, ISMARClubType.SINGLE_SHOT_AUTHOR]

    @staticmethod
    def size():
        return 5

class ISMARAuthor:

    first_name = ""
    last_name = ""

    country = ""

    id = -1   # id is assigned during the analysis of the data.
    papers = 0 # number of papers published at ISMAR

    # a list of the paper ids (myid) of this author
    paper_list = None

    # author ISMARClubType
    club_type = None

    # list of co-authors
    coauthors = None


    def __init__(self):
        pass



class ISMAREntry:


    data = None
    authors = None
    title = ""
    id = -1  # IEEE id.
    year = 0

    is_TVCG = False

    myid = -1 # my id counter.

    first_author_last = ""
    first_author_first = ""

    def __init__(self):
        authors = list()
        data = dict()



class ISMAR_DB:


    db = []

    def __init__(self):
        pass


    def size(self):
        return len(self.db)



    def has_key(self, key):

        if key in self.db:
            return True
        else:
            return False