/* rendering user-names who have liked the post  */
SELECT
    Name
FROM
    Person
    JOIN Person_Likes_Post ON Person.kerberosID = Person_Likes_Post.kerberosID
WHERE
    Person_Likes_Post.postID = :givenPostID;



SELECT
    post.postid,
    post.postedby,
    COUNT(person_likes_post.kerberosid) AS like_count,
    post.caption,
    (SELECT COUNT(*) FROM person_likes_post WHERE post.postid = person_likes_post.postid AND person_likes_post.kerberosID = %s) AS user_like_count
FROM
    post
    LEFT JOIN person_likes_post ON post.postid = person_likes_post.postid
    LEFT JOIN person ON person_likes_post.kerberosid = person.kerberosid
WHERE
    post.belongstogroups IS NULL
    AND post.postedby = %s
GROUP BY
    post.postid;
