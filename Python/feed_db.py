# Cassandra driver
from cassandra.cluster import Cluster

# UUID generator
from uuid import uuid1

# Other utils
from random import choice, randint
from datetime import datetime
import string


class Student:

    def __init__(self, id_student, first_name, last_name, mail, promotion):
        self.id_student = id_student
        self.first_name = first_name
        self.last_name = last_name
        self.mail = mail
        self.promotion = promotion

    def __str__(self):
        # Automatically used when 'execute' is called to generate the CQL query.
        return "{id_student : " + str(self.id_student) +\
               ", first_name : '" + self.first_name +\
               "', last_name : '" + self.last_name +\
               "', mail : '" + self.mail +\
               "', promotion : '" + self.promotion +\
               "'}"

    @staticmethod
    def student_from_select(row_student):
        return Student(
            row_student.id_student,
            row_student.first_name,
            row_student.last_name,
            row_student.mail,
            row_student.promotion)


class Course:
    def __init__(self, id_course, name, allocated_hours, referent_teacher):
        self.id_course = id_course
        self.name = name
        self.allocated_hours = allocated_hours
        self.referent_teacher = referent_teacher

    def __str__(self):
        # Automatically used when 'execute' is called to generate the CQL query.
        return "{id_course : " + str(self.id_course) +\
               ", name : '" + self.name +\
               "', allocated_hours : " + str(self.allocated_hours) +\
               ", referent_teacher : '" + self.referent_teacher +\
               "'}"

    @staticmethod
    def course_from_select(row_course):
        return Course(
            row_course.id_course,
            row_course.name,
            row_course.allocated_hours,
            row_course.referent_teacher
        )


class Schedule_Entry:
    def __init__(self, date, duration, room):
        self.date = date
        self.duration = duration
        self.room = room

    def __str__(self):
        # Automatically used when 'execute' is called to generate the CQL query.
        return "{date : '" + str(self.date) + \
               "', duration : " + self.duration + \
               ", room : '" + self.room + \
               "'}"


def init_cassandra():
    cluster = Cluster()
    session = cluster.connect()

    # Select emse keyspace
    session.set_keyspace('emse')

    return session


def add_courses(session):

    courses =\
        [Course(uuid1(), "Majeure Info", 159, "Jean"),
         Course(uuid1(), "Défi Big Data", 78, "Robert"),
         Course(uuid1(), "TB3 IA", 90, "Martin"),
         Course(uuid1(), "TB1 Traitement d_images", 40, "Paul")]

    print("Adding following entries to students_by_course : \n" + str(courses))

    # Add entries to table students_by_course
    for course in courses:
        session.execute(
            """
            INSERT INTO students_by_course (course)
            VALUES (%s)
            """,
            (course,)
            )


def add_students(session, entries_number=500):
    promotions = ("1A", "2A", "3A")

    # Add entries to table Student
    students = []

    courses = [Course.course_from_select(row.course)
               for row in session.execute("SELECT course FROM students_by_course")]

    for i in range(entries_number):

        ID_Student = uuid1()
        First_Name = "".join(choice(string.ascii_letters) for x in range(randint(5, 12)))
        Last_Name = "".join(choice(string.ascii_letters) for x in range(randint(5, 12)))
        Last_Name = Last_Name.upper()
        First_Name = First_Name.capitalize()
        Mail = First_Name.lower() + "." + First_Name.lower() + "@etu.emse.fr"
        Promotion = promotions[randint(0, 2)]

        Taken_Courses = []
        for course in courses:
            if randint(0, 1):
                Taken_Courses.append(course)

        students.append((Student(ID_Student, First_Name, Last_Name, Mail, Promotion), set(Taken_Courses)))

    print("Adding " + str(entries_number) + " random students to Student...")
    begin = datetime.now()

    for student in students:

        # Add entries to courses_by_student
        session.execute(
            """
            INSERT INTO courses_by_student (student, taken_courses)
            VALUES (%s, %s)
            """,
            student
        )

        # Update students_by_course
        for course in student[1]:
            session.execute(
                """
                UPDATE students_by_course SET students = students + {%s} WHERE course = %s
                """,
                (student[0], course)
            )

    end = datetime.now()
    print(str(entries_number) + " random students added in " + str((end - begin).total_seconds()) + " seconds.")


def add_schedule(session, entries_number_per_course=100):
    from datetime import datetime
    from random import randint

    blocks = ['D', 'A', 'E', 'F', 'G', 'H', 'J']

    schedule_entries = {}
    duration = "3h15m"  # A course duration as represented in CQL

    courses = [Course.course_from_select(row.course)
               for row in session.execute("SELECT course FROM students_by_course")]

    mid = int(entries_number_per_course / 2)

    for course in courses:
        schedule_entries[course] = []
        for j in range(mid):
            dt = datetime(2018, randint(1, 12), randint(1, 28), hour=8, minute=15)
            room = blocks[randint(0, 6)] + str(randint(0, 3)) + str(randint(0, 30))
            item = Schedule_Entry(dt, duration, room)
            schedule_entries[course].append(item)

        for j in range(mid, entries_number_per_course):
            dt = datetime(2018, randint(1, 12), randint(1, 28), hour=13, minute=30)
            room = blocks[randint(0, 6)] + str(randint(0, 3)) + str(randint(0, 30))
            item = Schedule_Entry(dt, duration, room)
            schedule_entries[course].append(item)

    total_hours = sum([len(schedule_entries[course]) for course in schedule_entries.keys()])
    print("Adding " + str(total_hours) + " random hours to Schedule...")
    begin = datetime.now()

    for course in schedule_entries.keys():

        schedule_entry_set = set(schedule_entries[course])

        # Add schedule to students_by_course
        session.execute(
            """
            UPDATE students_by_course SET schedule = %s WHERE course = %s
            """,
            (schedule_entry_set, course)
        )

        # Update courses_by_students
        for student in [Student.student_from_select(row.student)
                        for row in session.execute("SELECT student FROM courses_by_student")]:

            schedule_entry_str = "{"
            for schedule_entry in schedule_entry_set:
                schedule_entry_str += str(schedule_entry) + ", "
            schedule_entry_str = schedule_entry_str[0:-2] + "}"

            session.execute(
                "UPDATE courses_by_student "
                "SET schedule[" + str(course) + "] = " + schedule_entry_str + " WHERE student = " + str(student))

            # Usual method doesn't work for obscure reasons, so CQL request has been generated manually above.
#             session.execute(
#                 """
#                 UPDATE courses_by_student SET schedule[%(course)s] = %(schedule_entry_set)s WHERE student = %(student)s
# 1               """,
#                 {'course': course, 'schedule_entry_set': schedule_entry_set, 'student': student}
#             )

    end = datetime.now()
    print(str(total_hours) + " random hours added in "
          + str((end - begin).total_seconds()) + " seconds.")


def add_results(session, results_number_by_course=10):
    students = session.execute(
        """
        SELECT student, taken_courses FROM courses_by_student
        """)

    results = {}
    for row in students:
        student = Student.student_from_select(row.student)
        results[student] = {}
        if row.taken_courses is not None:
            for row_course in row.taken_courses:
                course = Course(
                    row_course.id_course,
                    row_course.name,
                    row_course.allocated_hours,
                    row_course.referent_teacher)
                marks = [randint(0, 20) for i in range(results_number_by_course)]
                results[student][course] = marks

    total_results = sum([len(results[student]) for student in results.keys()])
    print("Adding " + str(total_results) + " random hours to Schedule...")
    begin = datetime.now()
    for student in results.keys():
        for course in results[student].keys():
            session.execute(
                """
                UPDATE courses_by_student SET results[%s] = %s WHERE student = %s
                """,
                (course, results[student][course], student)
            )

    end = datetime.now()
    print(str(total_results) + " random results added in "
          + str((end - begin).total_seconds()) + " seconds.")


def clear_all(session):
    print("Clearing courses_by_students...")
    session.execute("TRUNCATE courses_by_student")
    print("Clearing students_by_course...")
    session.execute("TRUNCATE students_by_course")


def main():
    session = init_cassandra()
    clear_all(session)
    add_courses(session)
    add_students(session, entries_number=5000)
    add_results(session, results_number_by_course=20)
    add_schedule(session, entries_number_per_course=50)


if __name__ == "__main__":
    main()

