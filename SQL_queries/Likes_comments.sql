/* rendering user-names who have liked the comment  */
SELECT
    Name
FROM
    Person
    JOIN Person_Likes_Comment ON Person.kerberos_ID = Person_Likes_Comment.kerberos_ID
WHERE
    Person_Likes_Comment.commentID = :givenCommentID