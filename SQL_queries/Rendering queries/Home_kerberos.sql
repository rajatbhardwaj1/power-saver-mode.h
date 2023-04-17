/* Rendering person's name and Kerberos*/
SELECT
    Name,
    Kerberos_ID
FROM
    Person
WHERE
    kerberos_ID = :givenID;

/* Rendering Posts  */
SELECT
    image,
    caption
FROM
    Posts
WHERE
    postedBy = :givenID
    AND belongsToGroups IS NULL;