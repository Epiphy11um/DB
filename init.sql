CREATE TABLE User (
    `UserID` INT PRIMARY KEY AUTO_INCREMENT,
    `UserName` VARCHAR(256) NOT NULL,
    `Password` VARCHAR(256) NOT NULL,
    `RealName` VARCHAR(64),
    `Age` INT,
    `Job` VARCHAR(32),
    `EducationLevel` VARCHAR(32),
    `Type` VARCHAR(16) NOT NULL
);

-- 乐队表
CREATE TABLE Band (
    BandID INT PRIMARY KEY AUTO_INCREMENT, -- 主键：乐队的唯一标识符
    BandName VARCHAR(100) NOT NULL, -- 乐队名称
    BandDescription TEXT, -- 乐队的介绍或简介
    FormationDate DATE -- 乐队成立时间
);

CREATE TABLE _UserToBand (
    `UserID` INT NOT NULL,
    `BandID` INT NOT NULL,
    `Role` VARCHAR(128),
    PRIMARY KEY (BandID, UserID), -- 联合主键：乐队ID和成员ID的组合
    FOREIGN KEY (BandID) REFERENCES Band(BandID), -- 外键约束，引用乐队表的BandID
    FOREIGN KEY (UserID) REFERENCES User(UserID) -- 外键约束，引用成员表的MemberID
);

-- 专辑表
CREATE TABLE Album (
    AlbumID INT PRIMARY KEY AUTO_INCREMENT, -- 主键：专辑的唯一标识符
    AlbumName VARCHAR(100) NOT NULL, -- 专辑名称
    AlbumDescription TEXT, -- 专辑文案或描述
    ReleaseDate DATE, -- 专辑发表时间
    BandID INT, -- 外键：关联乐队表
    FOREIGN KEY (BandID) REFERENCES Band(BandID) -- 外键约束，引用乐队表的BandID
);

-- 演唱会表
CREATE TABLE Concert (
    ConcertID INT PRIMARY KEY AUTO_INCREMENT, -- 主键：演唱会的唯一标识符
    ConcertName VARCHAR(100) NOT NULL, -- 演唱会名称
    Location VARCHAR(200), -- 举办地点
    ConcertDate DATETIME, -- 举办时间
    BandID INT, -- 外键：关联乐队表
    FOREIGN KEY (BandID) REFERENCES Band(BandID) -- 外键约束，引用乐队表的BandID
);

-- 歌曲表
CREATE TABLE Song (
    SongID INT PRIMARY KEY AUTO_INCREMENT, -- 主键：歌曲的唯一标识符
    SongName VARCHAR(100) NOT NULL, -- 歌曲名称
    OriginalAuthor VARCHAR(100), -- 歌曲原作者
    Genre VARCHAR(50), -- 歌曲风格
    AlbumID INT,
    `Order` INT,
    FOREIGN KEY (AlbumID) REFERENCES Album(AlbumID)
);

-- 乐评表
CREATE TABLE Review (
    AlbumID INT, -- 外键：关联歌曲表
    UserID INT, -- 外键：关联歌迷表
    Rating INT, -- 评分
    Comment TEXT, -- 评论
    PRIMARY KEY (AlbumID, UserID), -- 联合主键：歌曲ID和歌迷ID的组合
    FOREIGN KEY (AlbumID) REFERENCES Album(AlbumID), -- 外键约束，引用歌曲表的SongID
    FOREIGN KEY (UserID) REFERENCES User(UserID) -- 外键约束，引用歌迷表的UserID
);

-- 参加表
CREATE TABLE Participation (
    ConcertID INT, -- 外键：关联演唱会表
    UserID INT, -- 外键：关联歌迷表
    TicketNumber VARCHAR(50), -- 票号
    PRIMARY KEY (ConcertID, UserID), -- 联合主键：演唱会ID和歌迷ID的组合
    FOREIGN KEY (ConcertID) REFERENCES Concert(ConcertID), -- 外键约束，引用演唱会表的ConcertID
    FOREIGN KEY (UserID) REFERENCES User(UserID) -- 外键约束，引用歌迷表的UserID
);

-- 喜欢A表
CREATE TABLE LikeBand (
    UserID INT, -- 外键：关联歌迷表
    BandID INT, -- 外键：关联乐队表
    PRIMARY KEY (UserID, BandID), -- 联合主键：歌迷ID和乐队ID的组合
    FOREIGN KEY (UserID) REFERENCES User(UserID), -- 外键约束，引用歌迷表的UserID
    FOREIGN KEY (BandID) REFERENCES Band(BandID) -- 外键约束，引用乐队表的BandID
);

-- 喜欢B表
CREATE TABLE LikeAlbum (
    UserID INT, -- 外键：关联歌迷表
    AlbumID INT, -- 外键：关联专辑表
    PRIMARY KEY (UserID, AlbumID), -- 联合主键：歌迷ID和专辑ID的组合
    FOREIGN KEY (UserID) REFERENCES User(UserID), -- 外键约束，引用歌迷表的UserID
    FOREIGN KEY (AlbumID) REFERENCES Album(AlbumID) -- 外键约束，引用专辑表的AlbumID
);

-- 喜欢C表
CREATE TABLE LikeSong (
    UserID INT, -- 外键：关联歌迷表
    SongID INT, -- 外键：关联歌曲表
    PRIMARY KEY (UserID, SongID), -- 联合主键：歌迷ID和歌曲ID的组合
    FOREIGN KEY (UserID) REFERENCES User(UserID), -- 外键约束，引用歌迷表的UserID
    FOREIGN KEY (SongID) REFERENCES Song(SongID) -- 外键约束，引用歌曲表的SongID
);