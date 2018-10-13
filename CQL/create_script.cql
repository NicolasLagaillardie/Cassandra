CREATE KEYSPACE emse WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}  AND durable_writes = true;

CREATE TYPE emse.course (
    id_course uuid,
    name text,
    allocated_hours int,
    referent_teacher text
);

CREATE TYPE emse.schedule_entry (
    date timestamp,
    duration duration,
    room text
);

CREATE TYPE emse.student (
    id_student uuid,
    first_name text,
    last_name text,
    mail text,
    promotion text
);

CREATE TABLE emse.courses_by_student (
    student frozen<student> PRIMARY KEY,
    results map<frozen<course>, frozen<list<decimal>>>,
    schedule map<frozen<course>, frozen<set<frozen<schedule_entry>>>>,
    taken_courses set<frozen<course>>
);

CREATE TABLE emse.students_by_course (
    course frozen<course> PRIMARY KEY,
    schedule set<frozen<schedule_entry>>,
    students set<frozen<student>>
);

