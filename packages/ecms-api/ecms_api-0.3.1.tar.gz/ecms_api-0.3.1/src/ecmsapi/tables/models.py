from ._base import TableMixin

__all__ = ['HRTEMP', 'HRTCPR']

import datetime


class HRTEMP(TableMixin):

    TABLE_NAME = 'HRTEMP'

    HRTEMPID = ('INT', 18)
    STATUSCODE = ('CHAR', 1)
    SRCCNCID = ('INT', 18)
    COMPANYNO = ('DEC', 2)
    DIVISIONNO = ('DEC', 3)
    CHGCNCID = ('INT', 18)
    CHGCOMPANY = ('INT', 2)
    CHGDIVISION = ('DEC', 3)
    EMPCNCID = ('INT', 18)
    EMPCOMPANY = ('DEC', 2)
    EMPDIVISION = ('DEC', 3)
    PRTMSTID = ('INT', 18)
    EMPLOYEENO = ('INT', 9)
    SOCIALSECNO = ('DEC', 9)
    EMPLNAME = ('CHAR', 30)
    ABBRV = ('CHAR', 10)
    ADDR1 = ('CHAR', 30)
    ADDR2 = ('CHAR', 30)
    ADDR3 = ('CHAR', 30)
    CITY = ('CHAR', 20)
    STATECODE = ('CHAR', 2)
    ZIPCODE = ('DEC', 3)
    COUNTRYCODE = ('DEC', 3)
    AREACODE = ('DEC', 3)
    PHONENO = ('DEC', 7)
    CELLPHAC = ('DEC', 3)
    CELLPHNO = ('DEC', 7)
    CONTACTNAME = ('CHAR', 30)
    CONTACTAC = ('DEC', 3)
    CONTACTPHONE = ('DEC', 7)
    BUSUFFIX = ('CHAR', 4)
    CNTRYCODE = ('CHAR', 3)
    MARITALSTAT = ('CHAR', 1)
    LVLCODE = ('DEC', 2)
    OFFICERSCODE = ('CHAR', 1)
    HRTOCCID = ('INT', 18)
    OCCUPDESC1 = ('CHAR', 20)
    OCCUPDESC2 = ('CHAR', 20)
    SEXCODE = ('CHAR', 1)
    MINORITYCODE = ('DEC', 1)
    HANDICAPCODE = ('CHAR', 1)
    DISABLEVEL = ('CHAR', 2)
    BLOODTYPE = ('CHAR', 3)
    BIRTHPLACE = ('CHAR', 25)
    PERMRESIDENT = ('CHAR', 1)
    DRIVERLICNO = ('CHAR', 25)
    DLNUMBER = ('CHAR', 8)
    BIRTHDATE = ('DATE', )
    ORIGHIREDATE = ('DATE', )
    ADJHIREDATE = ('DATE', )
    VACELIGDATE = ('DATE', )
    LASTYEDATE = ('DATE', )
    ELIGSCKACCRL = ('DATE', )
    SICKACRLDATE = ('DATE', )
    EXPRIEDATE = ('DATE', )
    RETIREDDATE = ('DATE', )
    VISAEXPDATE = ('DATE', )
    REVIEWDATE = ('DATE', )
    ESTAVAILDATE = ('DATE', )
    ISSUEI9DATE = ('DATE', )
    I9EXPDATE = ('DATE', )
    ISSUEI9 = ('CHAR', 1)
    COBRALTRDATE = ('DATE', )
    COBRALTRRCVD = ('DATE', )
    COBREASNTFLG = ('CHAR', 1)
    REHIREDATE = ('DATE', )
    HOLELIGDATE = ('DATE', )
    DISABILITYDT = ('DATE', )
    TERMDATE = ('DATE', )
    PRTTRMID = ('INT', 18)
    TERMCODE = ('DEC', 2)
    LASTDAYWK = ('DATE', )
    BENEFITGP = ('CHAR', 50)
    ISSUEAUTH = ('CHAR', 25)
    EVERIFYDT = ('DATE', )
    EVERCASE = ('CHAR', 15)
    EVERCRES = ('CHAR', 25)
    TERMRSN = ('DEC', 3)
    ELGBRHIRE = ('CHAR', 1)
    PRTLBRID = ('INT', 18)
    DEPTNO = ('DEC', 3)
    PRTECLID = ('INT', 18)
    EMPLCLASS = ('DEC', 3)
    EMPLTYPE = ('CHAR', 2)


class HRTCPR(TableMixin):

    TABLE_NAME = 'HRTCPR'
    
    HRTCPRID = ('INT', 18)
    STATUSCODE = ('CHAR', 1)
    SRCCNCID = ('INT', 18)
    COMPANYNO = ('INT', 2)
    DIVISIONNO = ('INT', 3)
    HRTEMPID = ('INT', 18)
    CONTROLNO = ('INT', 20)
    PROPERTYNO = ('INT', 3)
    DESCRIPTION = ('CHAR', 50)
    ASGDATE = ('DATE',)
    RTNDATE = ('DATE',)
    EXPDATE = ('DATE',)
    DUEDATE = ('DATE',)
    RETIREDDATE = ('DATE',)
    APTVENID = ('INT', 18)
    VENDORNO = ('INT', 5)
    PROPAMOUNT = ('INT', 9)
    RETURNEDTO = ('CHAR', 20)
    ADDEDBY = ('CHAR', 20)
    ADDEDDATE = ('TIMESTAMP', 26)
    UPDPGM = ('CHAR', 20)
    UPDATEDBY = ('CHAR', 20)
    UPDDATE = ('TIMESTAMP', 26)

    DEFAULTS = [
            ('STATUSCODE', 'A' ),
            ('SRCCNCID', '5'),
            ('COMPANYNO', '1'),
            ('DIVISIONNO', '0'),
            ('ASGDATE', datetime.date.today()),
            ('UPDPGM', 'HRTP130'),
            ('UPDATEDBY', 'CGCOWNER'),
        ]

    FORIEGN_KEYS = [
        {'EMPLOYEENO': {'table': HRTEMP, 'ref': 'HRTEMPID' }},
    ]


