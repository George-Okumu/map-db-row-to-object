from config import CONN, CURSOR
from mentor import Mentor;


class Student(Mentor):
    SCORE = 0 # class variable

    def __init__(self, name, age, mentor) -> None:
        self.id = None
        super().__init__(name, age) # inheriting from base class
        self.mentor = mentor
        if not self.check_mentor_exists():
            raise ValueError(f"Mentor ID {self.mentor} does not exist.")

    
    # check if mentor exists before creating a student
    def check_mentor_exists(self):
        mentor_exists = CURSOR.execute("SELECT COUNT(*) FROM mentors WHERE id = ?", (self.mentor,)).fetchone()[0]
        return mentor_exists > 0
    
    
    # ORM writting
    # mapping class to database
    @classmethod
    def create_table(cls):
        sql_query = """
                CREATE TABLE IF NOT EXISTS students(
                id integer primary key,
                name varchar,
                age integer,
                mentor_id integer
                ) 
            """
        CURSOR.execute(sql_query)
        print("Table Created successfully")

      
    def save(self):
        sql_query = """
                    INSERT INTO students (name, age, mentor_id) VALUES (?, ?, ?)
                """
        CURSOR.execute(sql_query, (self.name, self.age, self.mentor))
        CONN.commit()

        
    @classmethod
    def drop_table(cls):
        CURSOR.execute(""" DROP TABLE students """)


    # mapping table rows into class objects
        
    @classmethod
    def list_all_students(cls):
        query_from_db = CURSOR.execute(""" select * from students """).fetchall()

        students_list = []
        for row in query_from_db:
            student = cls(row[1], row[2], row[3])
            student.id = row[0]
            students_list.append(student.__dict__)
        
        return students_list
        
        
    @classmethod
    def list_all_students_for_a_specific_mentor(cls, mentor_name):
        all_students = []
        rows_from_db = CURSOR.execute("""
            SELECT s.id, s.name, s.age
            FROM students s
            LEFT JOIN mentors m ON s.mentor_id = m.id
            WHERE m.name = ?
        """, (mentor_name,)).fetchall()

        for row in rows_from_db:
            # directly create dictionary to store only student age, and name instead of mapping it tostudent
            student_data = {
                "id": row[0],
                "name": row[1],
                "age": row[2]
            }
            all_students.append(student_data)
        
        return all_students
    

    