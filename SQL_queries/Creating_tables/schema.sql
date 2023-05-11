CREATE TABLE Person (
  kerberosID char(10) PRIMARY KEY,
  name varchar,
  hostel varchar,
  gender char(1)
);
CREATE TABLE Passwords (
  kerberosID char(10) PRIMARY KEY,
  pass varchar
);

CREATE TABLE Post(postID char(8) PRIMARY KEY,
  image bytea,  
  caption varchar,  
  postedBy char(10),  
  belongsToGroups char(8));


CREATE TABLE Groups (
  groupID char(8) PRIMARY KEY,
  type char(20),
  hostel_department char(20),
  title varchar,
  moderator char(10)
);

CREATE TABLE Person_Belongsto_Group (
  kerberosID char(10),
  groupID char(8),
  PRIMARY KEY (kerberosID, groupID)
);


CREATE TABLE Comments (
  commentID char(8) PRIMARY KEY,
  content varchar,
  creatorPersonID char(10),
  parentPostID char(8),
  parentCommentID char(8)
);

CREATE TABLE Person_Likes_Post (
  kerberosID char(8),
  postID char(8),
  PRIMARY KEY (kerberosID, postID)
);

CREATE TABLE Person_Likes_Comment (
  kerberosID char(10),
  commentID char(8),
  PRIMARY KEY (kerberosID, commentID)
);

CREATE TABLE Friends (
  person1 char(10),
  person2 char(10),
  PRIMARY KEY (person1, person2)
);

ALTER TABLE Groups ADD FOREIGN KEY (moderator) REFERENCES Person (kerberosID);

ALTER TABLE Person_Belongsto_Group ADD FOREIGN KEY (kerberosID) REFERENCES Person (kerberosID);

ALTER TABLE Person_Belongsto_Group ADD FOREIGN KEY (groupID) REFERENCES Groups (groupID);

ALTER TABLE Post ADD FOREIGN KEY (postedBy) REFERENCES Person (kerberosID);

ALTER TABLE Post ADD FOREIGN KEY (belongsToGroups) REFERENCES Groups (groupID);

ALTER TABLE Comments ADD FOREIGN KEY (creatorPersonID) REFERENCES Person (kerberosID);

ALTER TABLE Comments ADD FOREIGN KEY (parentPostID) REFERENCES Post (postID);

ALTER TABLE Comments ADD FOREIGN KEY (parentCommentID) REFERENCES Comments (commentID);

ALTER TABLE Person_Likes_Post ADD FOREIGN KEY (kerberosID) REFERENCES Person (kerberosID);

ALTER TABLE Person_Likes_Post ADD FOREIGN KEY (postID) REFERENCES Post (postID);

ALTER TABLE Person_Likes_Comment ADD FOREIGN KEY (kerberosID) REFERENCES Person (kerberosID);

ALTER TABLE Person_Likes_Comment ADD FOREIGN KEY (commentID) REFERENCES Comments (commentID);

ALTER TABLE Friends ADD FOREIGN KEY (person1) REFERENCES Person (kerberosID);

ALTER TABLE Friends ADD FOREIGN KEY (person2) REFERENCES Person (kerberosID);

ALTER TABLE passwords ADD FOREIGN KEY (kerberosID) REFERENCES Person (kerberosID);
