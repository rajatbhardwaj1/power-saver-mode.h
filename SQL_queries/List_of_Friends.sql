-- List of friends of a person
SELECT
    Friends.Person1,
    Person.name
FROM
    Friends
    JOIN Person ON Friends.Person1 = Person.KerberosID
WHERE
    Friends.Person2 = :given_person_ID
UNION
SELECT
    Friends.Person2,
    Person.name
FROM
    Friends
    JOIN Person ON Friends.Person2 = Person.KerberosID
WHERE
    Friends.Person1 = :given_person_ID
    