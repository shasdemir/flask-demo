drop table if EXISTS entries;
create table entries (
    id integer primary key autoincrement,
    title text not null,
    text text not null
);