CREATE INDEX person_kerberosid on person(kerberosID);
CREATE INDEX post_postid on post(postID);
CREATE INDEX groups_groupid on groups(groupid);
CREATE INDEX Person_Belongsto_Group_groupid on Person_Belongsto_Group(groupid);
CREATE INDEX Person_Belongsto_Group_kerbId on Person_Belongsto_Group(kerberosID);
CREATE INDEX Comments_commentID on Comments(commentID);
CREATE INDEX Comments_createrid on Comments(creatorPersonID);
CREATE INDEX Comments_parentpostid on Comments(parentPostID);
CREATE INDEX Comments_parentcommentid on Comments(parentCommentID);
CREATE INDEX Person_Likes_Post_kerb on Person_Likes_Post(kerberosID);
CREATE INDEX Person_Likes_Post_postid on Person_Likes_Post(postID);
CREATE INDEX Person_Likes_comment_kerb on Person_Likes_Comment(kerberosID);
CREATE INDEX Person_Likes_comment_commentid on Person_Likes_Comment(commentID);
CREATE INDEX Friends_person1 on Friends(person1);
CREATE INDEX Friends_person2 on Friends(person2);

