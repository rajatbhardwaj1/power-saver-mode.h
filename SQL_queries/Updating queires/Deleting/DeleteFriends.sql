DELETE FROM
    Friends
WHERE
   ( Person1 = :Person1,
    AND Person2 = :Person2)
OR
   ( Person2 = :Person1,
    AND Person1 = :Person2);