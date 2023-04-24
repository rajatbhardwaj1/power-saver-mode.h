-- list of post in a particular group
SELECT
    image,
    caption,
    postedBy
FROM
    post
WHERE
    BelongsToGroups = :given_group_ID;