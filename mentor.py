from config import CONN, CURSOR
class Mentor:
    
    def __init__(self, name, age) -> None:
        self.id = None
        self.name = name
        self.age = age

    @classmethod
    def create_table(cls):
        sql = """
                create table if not exists mentors (
                    id integer primary key,
                    name vachar(30),
                    age integer
                )
            """
        CURSOR.execute(sql)
    
    def save(self):
        CURSOR.execute(""" insert into mentors(name, age) values (?, ?) """, (self.name, self.age))
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute(""" DROP TABLE students """)


    
    @classmethod
    def list_all_mentors(cls):
        query_from_db = CURSOR.execute(""" select * from mentors """).fetchall()

        mentors_list = []
        for row in query_from_db:
            mentor = cls(row[1], row[2])
            mentor.id = row[0]
            mentors_list.append(mentor.__dict__)
        
        return mentors_list
    
    @classmethod
    def find_mentor_by_name(cls, m_name):
        query_from_db = CURSOR.execute("""SELECT * FROM mentors WHERE name = ?""", (m_name,)).fetchall()

        found_list = []
        for row in query_from_db:
            mentors = cls(row[1], row[2])
            mentors.id = row[0]
            found_list.append(mentors.__dict__)
        
        return found_list or "No mentor/s with such name"
        

    # #list all students for a certain mentor
    def students_for_mentor(self):
        rows_from_db = CURSOR.execute(""" select * from students where mentor_id = ? """, (self.id,)).fetchall()
        students_list = []
        for row in rows_from_db:
            from student import Student

            student = Student(row[1], row[2], row[3])
            student.id = row[0]
            students_list.append(student.__dict__)
        
        return students_list
