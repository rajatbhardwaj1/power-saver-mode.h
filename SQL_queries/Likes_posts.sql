/* rendering user-names who have liked the post  */
SELECT
    Name
FROM
    Person
    JOIN Person_Likes_Post ON Person.kerberos_ID = Person_Likes_Post.kerberos_ID 
WHERE
    Person_Likes_Post.postID = :givenPostID
