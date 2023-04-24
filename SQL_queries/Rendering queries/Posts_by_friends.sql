-- list of post by all the friends of a person
SELECT
    post.image,
    post.caption,
    post.postedBy
FROM
    post
    JOIN Friends ON Friends.Person1 = post.postedBy
WHERE
    Friends.Person2 = :given_person_ID
UNION
SELECT
    post.image,
    post.caption,
    post.postedBy
FROM
    post
    JOIN Friends ON Friends.Person2 = post.postedBy
WHERE
    Friends.Person1 = :given_person_ID;


