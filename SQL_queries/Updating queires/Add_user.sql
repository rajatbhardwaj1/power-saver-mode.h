INSERT INTO
    Person
VALUES
    (
        :given_KerberosID,
        :given_name,
        :given_hostel,
        :given_gender
    );

INSERT INTO
    Person_Belongsto_Group
VALUES
    (
        :given_KerberosID,
        :groupID_dept
    );

INSERT INTO
    Person_Belongsto_Group
VALUES
    (
        :given_KerberosID, 
        :groupID_hostel
    );