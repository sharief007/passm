
drop table if exists CREDENTIALS;

create table CREDENTIALS (
    ID integer primary key autoincrement,
    APPLICATION_NAME text not null unique ,
    USERNAME text not null ,
    PASSWORD text not null ,
    CREATION_TIME timestamp
);

drop table if exists EMAILS;

create table EMAILS (
    ID integer primary key autoincrement ,
    CREDENTIALS_ID integer ,
    EMAIL_ADDRESS text ,
    foreign key (CREDENTIALS_ID) references CREDENTIALS(ID)
);

drop table if exists HOSTS;

create table HOSTS (
    ID integer primary key autoincrement ,
    CREDENTIALS_ID integer ,
    APPLICATION_HOST text ,
    foreign key (CREDENTIALS_ID) references CREDENTIALS(ID)
);

drop table if exists QUESTIONS;

create table QUESTIONS (
    ID integer primary key autoincrement ,
    CREDENTIALS_ID integer ,
    QUESTION text not null ,
    ANSWER text not null ,
    foreign key (CREDENTIALS_ID) references CREDENTIALS(ID)
);

drop table if exists INFO;

create table INFO (
    ID integer primary key autoincrement ,
    CREDENTIALS_ID integer ,
    INFO_KEY text not null ,
    INFO_VALUE text not null ,
    foreign key(CREDENTIALS_ID) references CREDENTIALS(ID)
)

