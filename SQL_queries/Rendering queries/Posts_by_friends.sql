-- list of posts by all the friends of a person
SELECT
    Posts.image,
    Posts.cation,
    Posts.postedBy
FROM
    Posts
    JOIN Friends ON Friends.Person1 = Posts.postedBy
WHERE
    Friends.Person2 = :given_person_ID
UNION
SELECT
    Posts.image,
    Posts.cation,
    Posts.postedBy
FROM
    Posts
    JOIN Friends ON Friends.Person2 = Posts.postedBy
WHERE
    Friends.Person1 = :given_person_ID;


