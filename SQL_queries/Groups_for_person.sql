-- List of groups in which the given person belongs
SELECT
    Groups.title
FROM
    Groups
    JOIN Person_Belongsto_Group ON Person_Belongsto_Group.GroupID = Groups.GroupID
WHERE
    Person_Belongsto_Group.KerberosID = :given_person_ID