COPY Person from '/home/project/power-saver-mode.h/data/Person.csv' DELIMITER ',' CSV HEADER;
COPY Groups from '/home/project/power-saver-mode.h/data/Groups.csv' DELIMITER ',' CSV HEADER;
COPY Person_Belongsto_Group from '/home/project/power-saver-mode.h/data/Person_Belongsto_Group.csv' DELIMITER ',' CSV HEADER;
COPY Comments from '/home/project/power-saver-mode.h/data/Comments.csv' DELIMITER ',' CSV HEADER;
COPY Person_Likes_Post from '/home/project/power-saver-mode.h/data/Person_Likes_Post.csv' DELIMITER ',' CSV HEADER;
COPY Person_Likes_Comment from '/home/project/power-saver-mode.h/data/Person_Likes_Comment.csv' DELIMITER ',' CSV HEADER;
COPY Friends from '/home/project/power-saver-mode.h/data/Friends.csv' DELIMITER ',' CSV HEADER;
COPY Posts from '/home/project/power-saver-mode.h/data/Posts.csv' DELIMITER ',' CSV HEADER; -> # wrote a python script for this because image needed to also be inserted