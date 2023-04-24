/* rendering comments with the users who have commented the post or comment */
SELECT
    Name , content 
FROM
    Person
    JOIN comments ON Person.kerberosid = comments.creatorPersonID 
WHERE
    comments.parentpostid = :given_post_or_commentID
    OR 
    comments.parentcommentid = :given_post_or_commentID;


