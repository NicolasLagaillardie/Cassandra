CREATE KEYSPACE emse WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}

CREATE TYPE emse.schedule_item (
    room text,
    course_duration duration
);

CREATE TABLE emse.course (
    id_course uuid PRIMARY KEY,
    allocated_hours int,
    name text,
    referent_teacher text
);

CREATE TABLE emse.result (
    id_result uuid PRIMARY KEY,
    id_course uuid,
    id_student uuid,
    results list<decimal>
);

CREATE TABLE emse.student (
    id_student uuid PRIMARY KEY,
    first_name text,
    last_name text,
    mail text,
    promotion text,
    results set<uuid>,
    taken_courses set<uuid>
);

CREATE TABLE emse.schedule (
    id_schedule uuid PRIMARY KEY,
    hours map<timestamp, frozen<schedule_item>>,
    id_course uuid
);
