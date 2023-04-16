DELETE FROM
    Person_Likes_Post
WHERE
    kerberos_ID = :kerberosID
    AND postID = :PostID;