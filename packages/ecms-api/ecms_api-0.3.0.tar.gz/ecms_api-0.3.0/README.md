# ECMS-API

ECMS-API is a query wrapper that allows for querying the AS400 directly

## Authors

**[Johnny Whitworth (@Poseidon-dev)](https://github.com/poseidon-dev)** 

## How to use Examples
SQLQuery is a class factory that takes in a table object. The methods in SQLQuery (select, update, insert)
return a class type of the same name with the table being passed as a paramter. 

It should be noted that the tables themselves are objects, and not strings. 

Tables can be found in ecmsapi


Select
```python
table = SQLQuery(HRTEMP)
query = table.select()

query.filters(employeeno=12345, companyno=50, divisionno=2)
query.columns(['CompanyNo', 'DivisionNo', 'EmployeeNo', 'City'])
query.order(by='City')
query.head()

response = query.query()

```

Returns the command and corresponding values:
```sql
SELECT
COMPANYNO, DIVISIONNO, EMPLOYEENO, CITY FROM CMSFIL.HRTEMP
WHERE EMPLOYEENO = '12345' AND COMPANYNO = '50' AND DIVISIONNO = '2' ORDER BY City ASC LIMIT 10
```

The select method also allows for queried data to be saved as an excel doc using .to_excel() rather than .query()


Update
```python
table = SQLQuery(HRTEMP)
query = table.update()

query.sets(City='SomeCity', companyno=50)
query.filters(employeeno=12345)
query.query()
```
Will execute the following:
```sql
UPDATE
CMSFIL.HRTEMP
SET CITY = 'SomeCity' , COMPANYNO = '50' WHERE EMPLOYEENO = '12345'
```

Insert
```python
table = SQLQuery(HRTCPR)
query = table.update()

query.sets(City='SomeCity', companyno=50)
query.filters(employeeno=12345)
query.query()
```
Will execute the following:
```sql
INSERT INTO
CMSFIL.HRTEMP
("CITY", "COMPANYNO") VALUES ('SomeCity', '50')
```

## Support

If you need some help for something, please reach out to me directly or submit an issue and I'll get to it as soon as I can

## Site

https://poseidon-dev.github.io/ecms-api/
