DELETE FROM
    Person_Likes_Post
WHERE
    kerberosid = :kerberosID
    AND postID = :PostID;