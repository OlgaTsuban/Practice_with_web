import argparse
from conf.db import session
from dateutil import parser as date_parser
from conf.models import Teacher, Student, Group, Subject, Mark

# Creates an object of define class
# Here is a logic for creating an objects in DB
def create_object(class_name, **name): 
    try:
        object = class_name(
            **name
        )
        session.add(object)
        session.commit()
        print(f"{class_name.__name__} created successfully.")
    except Exception as e:
        print(f"Error creating teacher: {str(e)}")
        session.rollback()

# Use query "SELECT * FROM class_name" to list information
# Here is a logic for getting all elements in {class_name} table
def list_elements(class_name):
    """SELECT * FROM teachers"""
    try:
        result = session.query(class_name).all()
        return result
    except Exception as e:
        print(f"Error retrieving elements: {str(e)}")
        session.rollback()
        return None

# Updates information in define class
#  Here is a logic for updating an elements in {class_name} table in DB
def update_object(class_name, object_id, **kwargs):
    try:
        obj = session.query(class_name).get(object_id)
        if obj:
            for key, value in kwargs.items():
                setattr(obj, key, value)

            session.commit()
            print(f"{(class_name.__name__)} with ID {object_id} updated successfully.")
        else:
            print(f"{class_name} with ID {object_id} not found.")
    except Exception as e:
        print(f"Error updating object: {str(e)}")
        session.rollback()


# Delete element from the table in DB
# Logic for removing object from DataBase
def remove_object(class_name, object_id):
    try:
        object = session.query(class_name).get(object_id)

        if object:
            session.delete(object)
            session.commit()
            print(f"{class_name.__name__} with ID {object_id} removed successfully.")
        else:
            print(f"{str(class_name)} with ID {object_id} not found.")
    except Exception as e:
        print(f"Error removing object: {str(e)}")
        session.rollback()

# Main function - has all logic 
def main():
    parser = argparse.ArgumentParser(description='CLI програма для CRUD операцій із базою даних.')
    parser.add_argument('--action', '-a', choices=['create', 'list', 'update', 'remove'], required=True, help='Дія: create, list, update, remove')
    parser.add_argument('--model', '-m', choices=['Teacher', 'Group', 'Student', 'Subject', 'Mark'], required=True, help='Модель для операції: Teacher')
    parser.add_argument('--id', type=int, help='Ідентифікатор запису')
    parser.add_argument('--group_id', type=int, help='Ідентифікатор запису групи')
    parser.add_argument('--teacher_id', type=int, help='Indentifier for teacher id')
    parser.add_argument('--student_id', type=int, help='Indentifier for student id')
    parser.add_argument('--subject_id', type=int, help='Indentifier for subject id')
    parser.add_argument('--date', type=lambda x: date_parser.parse(x).date(), help='Date for the operation')
    parser.add_argument('--name','-n', required=False, help='Ім\'я вчителя')
    parser.add_argument('--grade','-g', type=int, required=False, help='Grade')

    args = parser.parse_args()

    if args.action == 'create': # This part CREATE class objects
        if args.model == 'Teacher':
            create_object(Teacher,fullname= args.name)
        if args.model == 'Group':
            create_object(Group, name=args.name)
        if args.model == 'Student':
            create_object(Student, fullname=args.name, group_id=args.group_id)
        if args.model == 'Subject':
            create_object(Subject, name=args.name, teacher_id=args.teacher_id)
        if args.model == 'Mark':
            if (args.grade > 0 and args.grade < 101):
                create_object(Mark, grade=args.grade, grade_date=args.date, student_id=args.student_id, subject_id=args.subject_id)
            else: print("Impossible grade")

    elif args.action == 'list': # This part return LIST of objects
        if args.model == 'Teacher':
            print(list_elements(Teacher))
        if args.model == 'Group':
            print(list_elements(Group))
        if args.model == 'Student':
            print(list_elements(Student))
        if args.model == 'Subject':
            print(list_elements(Subject))
        if args.model == 'Mark':
            print(list_elements(Mark))

    elif args.action == 'update': # This part UPDATE some objects by id
        if args.model == 'Teacher':
            update_object(Teacher, args.id, fullname=args.name)
        if args.model == 'Group':
            update_object(Group, args.id, name=args.name)
        if args.model == 'Student':
            update_object(Student, args.id, fullname=args.name, group_id=args.group_id)
        if args.model == 'Subject':
            update_object(Subject,args.id, name=args.name, teacher_id=args.teacher_id)
        if args.model == 'Mark':
            if (args.grade > 0 and args.grade < 101):
                update_object(Mark, args.id, grade=args.grade, grade_date=args.date, student_id=args.student_id, subject_id=args.subject_id)
            else: print("Impossible grade")
        
    elif args.action == 'remove': # This part REMOVE some objects by id
        if args.model == 'Teacher':
            remove_object(Teacher, args.id)
        if args.model == 'Group':
            remove_object(Group, args.id)
        if args.model == 'Student':
            remove_object(Student, args.id)
        if args.model == 'Subject':
            remove_object(Subject, args.id)
        if args.model == 'Mark':
            remove_object(Mark, args.id)


if __name__ == '__main__':
    main()
