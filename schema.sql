CREATE TABLE "Person" (
  "kerberosID" varchar PRIMARY KEY,
  "name" varchar,
  "hostel" varchar,
  "gender" varchar,
  "email" varchar
);

CREATE TABLE "Groups" (
  "groupID" varchar PRIMARY KEY,
  "type" varchar,
  "hostel_department" varchar,
  "title" varchar,
  "moderator" varchar
);

CREATE TABLE "Person_Belongsto_Group" (
  "kerberosID" varchar,
  "groupID" varchar,
  PRIMARY KEY ("kerberosID", "groupID")
);

CREATE TABLE "Posts" (
  "postID" varchar PRIMARY KEY,
  "imageURL" varchar,
  "caption" varchar,
  "postedBy" varchar,
  "belongsToGroups" varchar
);

CREATE TABLE "Comments" (
  "commentID" varchar PRIMARY KEY,
  "content" varchar,
  "creatorPersonID" varchar,
  "parentPostID" varchar,
  "parentCommentID" varchar
);

CREATE TABLE "Person_Likes_Post" (
  "kerberosID" varchar,
  "postID" varchar,
  PRIMARY KEY ("kerberosID", "postID")
);

CREATE TABLE "Person_Likes_Comment" (
  "kerberosID" varchar,
  "commentID" varchar,
  PRIMARY KEY ("kerberosID", "commentID")
);

CREATE TABLE "Friends" (
  "person1" varchar,
  "person2" varchar,
  PRIMARY KEY ("person1", "person2")
);

ALTER TABLE "Groups" ADD FOREIGN KEY ("moderator") REFERENCES "Person" ("kerberosID");

ALTER TABLE "Person_Belongsto_Group" ADD FOREIGN KEY ("kerberosID") REFERENCES "Person" ("kerberosID");

ALTER TABLE "Person_Belongsto_Group" ADD FOREIGN KEY ("groupID") REFERENCES "Groups" ("groupID");

ALTER TABLE "Posts" ADD FOREIGN KEY ("postedBy") REFERENCES "Person" ("kerberosID");

ALTER TABLE "Posts" ADD FOREIGN KEY ("belongsToGroups") REFERENCES "Groups" ("groupID");

ALTER TABLE "Comments" ADD FOREIGN KEY ("creatorPersonID") REFERENCES "Person" ("kerberosID");

ALTER TABLE "Comments" ADD FOREIGN KEY ("parentPostID") REFERENCES "Posts" ("postID");

ALTER TABLE "Comments" ADD FOREIGN KEY ("parentCommentID") REFERENCES "Comments" ("commentID");

ALTER TABLE "Person_Likes_Post" ADD FOREIGN KEY ("kerberosID") REFERENCES "Person" ("kerberosID");

ALTER TABLE "Person_Likes_Post" ADD FOREIGN KEY ("postID") REFERENCES "Posts" ("postID");

ALTER TABLE "Person_Likes_Comment" ADD FOREIGN KEY ("kerberosID") REFERENCES "Person" ("kerberosID");

ALTER TABLE "Person_Likes_Comment" ADD FOREIGN KEY ("commentID") REFERENCES "Comments" ("commentID");

ALTER TABLE "Friends" ADD FOREIGN KEY ("person1") REFERENCES "Person" ("kerberosID");

ALTER TABLE "Friends" ADD FOREIGN KEY ("person2") REFERENCES "Person" ("kerberosID");
