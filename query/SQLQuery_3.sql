CREATE TABLE [User] (
    userID INT NOT NULL,
    SSN VARCHAR(17) NOT NULL,
    name VARCHAR(30) NOT NULL,
    birthDate DATE NOT NULL,
    gender VARCHAR(6) NOT NULL,
    username VARCHAR(30) NOT NULL,
    PRIMARY KEY (userID),
    UNIQUE (SSN),
    UNIQUE (username)
);

