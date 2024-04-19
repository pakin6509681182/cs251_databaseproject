-- CREATE TABLE PhoneNumber (
--     userID INT NOT NULL,
--     SSN VARCHAR(17) NOT NULL,
--     phone_number CHAR(12) NOT NULL,
--     CONSTRAINT PK_Phone_number PRIMARY KEY (userID, SSN, phone_number),
--     CONSTRAINT FK_Phone_number_UserID FOREIGN KEY (userID) REFERENCES [User](userID),
--     CONSTRAINT FK_Phone_number_SSN FOREIGN KEY (SSN) REFERENCES [User](SSN)
-- );

-- CREATE TABLE Member (
--     userID INT NOT NULL,
--     SSN VARCHAR(17) NOT NULL,
--     score SMALLINT,
--     CONSTRAINT PK_Member PRIMARY KEY (userID, SSN),
--     CONSTRAINT FK_Member_UserID FOREIGN KEY (userID) REFERENCES [User](userID),
--     CONSTRAINT FK_Member_SSN FOREIGN KEY (SSN) REFERENCES [User](SSN)
-- );

-- CREATE TABLE Exam (
--     userID INT NOT NULL,
--     SSN VARCHAR(17) NOT NULL,
--     score SMALLINT,
--     CONSTRAINT PK_Exam PRIMARY KEY (userID, SSN),
--     CONSTRAINT FK_Exam_UserID FOREIGN KEY (userID) REFERENCES [User](userID),
--     CONSTRAINT FK_Exam_SSN FOREIGN KEY (SSN) REFERENCES [User](SSN)
-- );

-- CREATE TABLE Admin (
--     userID INT NOT NULL,
--     SSN VARCHAR(17) NOT NULL,
--     CONSTRAINT PK_Admin PRIMARY KEY (userID, SSN),
--     CONSTRAINT FK_Admin_UserID FOREIGN KEY (userID) REFERENCES [User](userID),
--     CONSTRAINT FK_Admin_SSN FOREIGN KEY (SSN) REFERENCES [User](SSN)
-- );


-- CREATE TABLE Dog (
--     PetID INT NOT NULL,
--     CONSTRAINT PK_Dog PRIMARY KEY (PetID),
--     CONSTRAINT FK_Dog_PetID FOREIGN KEY (PetID) REFERENCES Pet(PetID),
-- );

-- CREATE TABLE Cat (
--     PetID INT NOT NULL,
--     CONSTRAINT PK_Cat PRIMARY KEY (PetID),
--     CONSTRAINT FK_Cat_PetID FOREIGN KEY (PetID) REFERENCES Pet(PetID),
-- );

-- CREATE TABLE FoundPlace (
--     userID INT NOT NULL,
--     SSN VARCHAR(17) NOT NULL,
--     PetID INT NOT NULL,
--     Province VARCHAR(30),
--     Street VARCHAR(30),
--     Zipcode VARCHAR(5),
--     Sub_district VARCHAR(30),
--     district VARCHAR(30),
--     CONSTRAINT PK_FoundPlace PRIMARY KEY (userID, SSN, PetID),
--     CONSTRAINT FK_FoundPlace_Member FOREIGN KEY (UserID, SSN) REFERENCES Member(UserID, SSN),
--     CONSTRAINT FK_FoundPlace_PetID FOREIGN KEY (PetID) REFERENCES Pet(PetID)
-- );

-- CREATE TABLE UserRequest (
--     requestID INT NOT NULL,
--     userID INT NOT NULL,
--     SSN VARCHAR(17) NOT NULL,
--     PetID INT NOT NULL,
--     date DATE,
--     approve_request BIT,
--     CONSTRAINT PK_UserRequest PRIMARY KEY (requestID, userID, SSN, PetID),
--     CONSTRAINT FK_UserRequest_Member FOREIGN KEY (UserID, SSN) REFERENCES Member(UserID, SSN),
--     CONSTRAINT FK_UserRequest_PetID FOREIGN KEY (PetID) REFERENCES Pet(PetID)
-- );





