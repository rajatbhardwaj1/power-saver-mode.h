DELETE FROM
    Person_Belongsto_Group
WHERE
    Kerberos_ID = :given_KerberosID
    AND groupID = :groupID;