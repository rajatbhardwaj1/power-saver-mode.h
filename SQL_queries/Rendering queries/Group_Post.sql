-- list of posts in a particular group
SELECT
    image,
    caption,
    postedBy
FROM
    Posts
WHERE
    BelongsToGroups = :given_group_ID;