/* rendering user-names who have liked the comment  */
SELECT
    Name
FROM
    Person
    JOIN Person_Likes_Comment ON Person.kerberosid = Person_Likes_Comment.kerberosid
WHERE
    Person_Likes_Comment.commentID = :givenCommentID;