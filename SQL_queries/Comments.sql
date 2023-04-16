/* rendering comments with the users who have commented the post or comment */
SELECT
    Name , content 
FROM
    Person
    JOIN comments ON Person.kerberos_ID = comments.creatorPersonID 
WHERE
    comments.commentID = :given_post_or_commentID

