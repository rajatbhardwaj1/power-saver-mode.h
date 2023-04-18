DELETE FROM
    Person_Likes_Comments
WHERE
    commentID = :given_commentID
    AND kerberosid = :given_KerberosID;