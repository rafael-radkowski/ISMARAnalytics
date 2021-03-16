


from enum import Enum

#Virbella, Recife, Brazil
#Bejing, China
#Munich, Germany
#Nantes, France
#Merida, Mexico.
#Fukuoka, Japan
#Munich, Germany
#Adelaide, Australia
#Atlanta, USA
#Basel, Switzerland
#Seoul, Korea (South)
#Orlando, FL, USA
#Cambridge, UK
#Nara, Japan
#Santa Barbara, CA, USA
#Vienna, Austria
#Arlington, VA, USA
#Tokyo, Japan
#Darmstadt, Germany


class ISMARLoc(Enum):


    RECIFE = 19
    BEIJING = 18
    MUNICH2 = 17
    NANTES = 16
    MERIDA = 15
    FUKUOKA = 14
    MUNICH1 = 13
    ADELEAIDE = 12
    ATLANTA = 11
    BASEL = 10
    SEOUL = 9
    ORANDO = 8
    CAMBRIDGE = 7
    NARA = 6
    SANTABARBARA = 5
    VIENNA = 4
    ARLINGTON = 3
    TOKYO = 2
    DARMSTADT = 1


    @staticmethod
    def yearToLoc(query_year):

        if query_year == 2002:
            return ISMARLoc.DARMSTADT
        elif query_year == 2003:
            return ISMARLoc.TOKYO
        elif query_year == 2004:
            return ISMARLoc.ARLINGTON
        elif query_year == 2005:
            return ISMARLoc.VIENNA
        elif query_year == 2006:
            return ISMARLoc.SANTABARBARA
        elif query_year == 2007:
            return ISMARLoc.NARA
        elif query_year == 2008:
            return ISMARLoc.CAMBRIDGE
        elif query_year == 2009:
            return ISMARLoc.ORANDO
        elif query_year == 2010:
            return ISMARLoc.SEOUL
        elif query_year == 2011:
            return ISMARLoc.BASEL
        elif query_year == 2012:
            return ISMARLoc.ATLANTA
        elif query_year == 2013:
            return ISMARLoc.ADELEAIDE
        elif query_year == 2014:
            return ISMARLoc.MUNICH1
        elif query_year == 2015:
            return ISMARLoc.FUKUOKA
        elif query_year == 2016:
            return ISMARLoc.MERIDA
        elif query_year == 2017:
            return ISMARLoc.NANTES
        elif query_year == 2018:
            return ISMARLoc.MUNICH2
        elif query_year == 2019:
            return ISMARLoc.BEIJING
        elif query_year == 2020:
            return ISMARLoc.RECIFE




    @staticmethod
    def getRegion(enumeration):

        if enumeration == ISMARLoc.DARMSTADT:
            return "Europe"
        elif enumeration == ISMARLoc.TOKYO:
            return "Asia/Pacific"
        elif enumeration == ISMARLoc.ARLINGTON:
            return "North America"
        elif enumeration == ISMARLoc.VIENNA:
            return "Euro"
        elif enumeration == ISMARLoc.SANTABARBARA:
            return "North America"
        elif enumeration == ISMARLoc.NARA:
            return "Asia/Pacific"
        elif enumeration == ISMARLoc.CAMBRIDGE:
            return "Europe"
        elif enumeration == ISMARLoc.ORANDO:
            return "North America"
        elif enumeration == ISMARLoc.SEOUL:
            return "Asia/Pacific"
        elif enumeration == ISMARLoc.BASEL:
            return "Europe"
        elif enumeration == ISMARLoc.ATLANTA:
            return "North America"
        elif enumeration == ISMARLoc.ADELEAIDE:
            return "Asia/Pacific"
        elif enumeration == ISMARLoc.MUNICH1:
            return "Europe"
        elif enumeration == ISMARLoc.FUKUOKA:
            return "Asia/Pacific"
        elif enumeration == ISMARLoc.MERIDA:
            return "South America"
        elif enumeration == ISMARLoc.NANTES:
            return "Europe"
        elif enumeration == ISMARLoc.MUNICH2:
            return "Europe"
        elif enumeration == ISMARLoc.BEIJING:
            return "Asia/Pacific"
        elif enumeration == ISMARLoc.RECIFE:
            return "South America"



    @staticmethod
    def toString( enumeration):

        if enumeration == ISMARLoc.DARMSTADT:
            return "Darmstadt, Germany"
        elif enumeration == ISMARLoc.TOKYO:
            return "Tokyo, Japan"
        elif enumeration == ISMARLoc.ARLINGTON:
            return "Arlington, VA, USA"
        elif enumeration == ISMARLoc.VIENNA:
            return "Vienna, Austria"
        elif enumeration == ISMARLoc.SANTABARBARA:
            return "Santa Barbara, CA, USA"
        elif enumeration == ISMARLoc.NARA:
            return "Nara, Japan"
        elif enumeration == ISMARLoc.CAMBRIDGE:
            return "Cambridge, UK"
        elif enumeration == ISMARLoc.ORANDO:
            return "Orlando, FL, USA"
        elif enumeration == ISMARLoc.SEOUL:
            return "Seoul, Korea (South)"
        elif enumeration == ISMARLoc.BASEL:
            return "Basel, Switzerland"
        elif enumeration == ISMARLoc.ATLANTA:
            return "Atlanta, USA"
        elif enumeration == ISMARLoc.ADELEAIDE:
            return "Adelaide, Australia"
        elif enumeration == ISMARLoc.MUNICH1:
            return "Munich, Germany"
        elif enumeration == ISMARLoc.FUKUOKA:
            return "Fukuoka, Japan"
        elif enumeration == ISMARLoc.MERIDA:
            return "Merida, Mexico"
        elif enumeration == ISMARLoc.NANTES:
            return "Nantes, France"
        elif enumeration == ISMARLoc.MUNICH2:
            return "Munich, Germany"
        elif enumeration == ISMARLoc.BEIJING:
            return "Bejing, China"
        elif enumeration == ISMARLoc.RECIFE:
            return "Virbella, Recife, Brazil"


    @staticmethod
    def yearToString(query_year):

        l = ISMARLoc.yearToLoc(query_year)
        return ISMARLoc.toString(l)



