-- list of posts in a particular group
SELECT
    imageURL,
    caption,
    postedBy
FROM
    Posts
WHERE
    BelongsToGroups = :given_group_ID