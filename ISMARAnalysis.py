



from ISMARTypes import ISMAR_DB
from ISMARLoader import LoadBibTex
from ISMARQuery import ISMARQuery


#db = ISMAR_DB()
#LoadBibTex("./data", ISMAR_DB)
#query =  ISMARQuery(db)

query =  ISMARQuery()
#query.AuthorFrequency()
#query.PaperFrequency()

# Print all papers for year
#query.PrintYear(2005)
#query.PrintKeywords(2013, 40)
#query.FirstAuthorFrequency()
#query.AverageAuthorsPerPaper()

# Print all the author network data
#uery.AllAuthorNetworks()
query.AuthorNetwork(2020, plot=False, with_BD = False)

# Get all publications in one year and their status.
query.PublicationsForYear(2020, True)

# Get all publications and their status statistics
#query.PublicationStatusStatistics()


# Get all the publications and their status for all years.
#query.PublicationClubStatus()

#query.FindAuthor("Klinker")
#query.FindAuthor("Kim")
#query.FindAuthor("Schall")

#query.FindAuthor("Alakhtar")

