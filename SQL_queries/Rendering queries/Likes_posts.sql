/* rendering user-names who have liked the post  */
SELECT
    Name
FROM
    Person
    JOIN Person_Likes_Post ON Person.kerberosID = Person_Likes_Post.kerberosID 
WHERE
    Person_Likes_Post.postID = :givenPostID;
