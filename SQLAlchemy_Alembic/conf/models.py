from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Presents the Teacher table, its param is id and fullname
class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<Teacher(id={self.id}, fullname={self.fullname})>"

# Presents the Group table, its param is id and name
class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<Group(id={self.id}, name={self.name})>"

# Presents the Student table, its param is id, fullname and group_id 
class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(100), nullable=False)
    group_id = Column('group_id', ForeignKey('groups.id', ondelete='CASCADE'))
    group = relationship('Group', backref='students')

    def __repr__(self):
        return f"<Student(id={self.id}, name={self.fullname}, group_id={self.group_id})>"

# Presents the Subject table, its param is id, name and teacher_id
class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    teacher_id = Column('teacher_id', ForeignKey('teachers.id', ondelete='CASCADE'))
    teacher = relationship('Teacher', backref='subjects')
    
    def __repr__(self):
        return f"<Subject(id={self.id}, name={self.name}, teacher_id={self.teacher_id})>"

# Presents the Mark table, its param is id, grade, grade_date, student_id and subject_id
class Mark(Base):
    __tablename__ = 'marks'
    id = Column(Integer, primary_key=True)
    grade = Column(Integer, nullable=False)
    grade_date = Column('grade_date', Date, nullable=True)
    student_id = Column('student_id', ForeignKey('students.id', ondelete='CASCADE'))
    subject_id = Column('subject_id', ForeignKey('subjects.id', ondelete='CASCADE'))
    student = relationship('Student', backref='grade')
    subject = relationship('Subject', backref='grade')

    def __repr__(self):
        return f"<Mark(id={self.id}, grade={self.grade}, grade_date={self.grade_date}, student_id={self.student_id}, subject_id={self.subject_id})>"