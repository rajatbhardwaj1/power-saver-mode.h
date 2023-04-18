/* Rendering person's name and Kerberos*/
SELECT
    Name,
    kerberosid
FROM
    Person
WHERE
    kerberosid = :givenID;

/* Rendering post  */
SELECT
    image,
    caption
FROM
    post
WHERE
    postedBy = :givenID
    AND belongsToGroups IS NULL;