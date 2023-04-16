DELETE FROM
    Person_Likes_Comments
WHERE
    commentID = :given_commentID
    AND kerberos_ID = :given_KerberosID;