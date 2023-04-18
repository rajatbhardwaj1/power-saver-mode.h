DELETE FROM
    Person_Belongsto_Group
WHERE
    kerberosid = :given_KerberosID
    AND groupID = :groupID;