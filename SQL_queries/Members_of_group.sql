-- List of person who are members of groups
SELECT
    Person.name,
    Person_Belongsto_Group.KerberosID
FROM
    Person
    JOIN Person_Belongsto_Group ON Person.KerberosID = Person_Belongsto_Group.KerberosID
WHERE
    Person_Belongsto_Group.GroupID = :given_group_ID