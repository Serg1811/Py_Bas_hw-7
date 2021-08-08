#!/usr/bin/env python
# coding: utf-8

# In[6]:


def average_grade_(grades):
    grades_list = []
    for course_grades in grades.values():
        grades_list += course_grades
    if len(grades_list) == 0:
        average_grade = None
    else:
        average_grade = round(sum(grades_list) / len(grades_list), 1)
    return average_grade

def average_grad_curses(list_name, curses):

    try:
        class_name = type(list_name[0])
    except:
        print('ОШИБКА: список имён пуст')
        return None
    grades_list = []
    names_without_grades = []
    names_without_curses = []
    for name in list_name:
        if type(name) == Reviewer:
            print('ОШИБКА: в списке присутствует имя эксперта')
            return None
        elif type(name) == class_name:
            if name.grades.get(curses) != None:
                if name.grades[curses] != 0:
                    grades_list += name.grades[curses]
                else:
                    names_without_grades += [name.name]
            else:
                names_without_curses += [name.name]
        else:
            print('ОШИБКА: в списке присутствуют имена разного класса')
            return None
    try:
        average_grade = round(sum(grades_list) / len(grades_list), 1)
    except:
        print(f"ОШИБКА: Оценок за курс {curses} пока нет")
        return None
    if len(names_without_curses) != 0:
        names_without_curses_str = '\n'.join(names_without_curses)
        if class_name == Student:
            print(f"Следующие студенты не проходили курс {curses}:\n{names_without_curses_str}")
        else:
            print(f"Следующие лекторы не преподоют курс {curses}:\n{names_without_curses_str}")
    if len(names_without_grades) != 0:
        names_without_grades_str ='\n'.join(names_without_grades)
        if class_name == Student:
            print(f"Следующие студенты не имеют оценок по курсу {curses}:\n{names_without_curses_str}")
        else:
            print(f"Следующие лекторы не имеют оценок по курсу {curses}:\n{names_without_curses_str}")
    print(f'средняя оценка за курс: {average_grade}\n')
    return average_grade

class Student:
    def __init__(self, name, surname, gender):
        self.name = name.title()
        self.surname = surname.title()
        self.gender = gender.lower()
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
    
    def courses(self, course):
        if course in self.finished_courses:
            print(f'\033[31mCтудент, {self.name} {self.surname}, уже прошёл курс {course}\033[0m\n')
        elif course in self.courses_in_progress:
            print(f'\033[31mCтудент, {self.name} {self.surname}, в настоящее время проходит курс {course}\033[0m\n')
        else:
            self.courses_in_progress += [course]
            print(f'\033[34mКурс, {course}, был успешно добавлен в програму обучения студента {self.name} {self.surname}\033[0m\n')
    def end_courses(self, course):
        if course in self.finished_courses:
            print(f'\033[31mCтудент, {self.name} {self.surname}, уже прошёл курс {course}\033[0m\n')
        elif course in self.courses_in_progress:
            self.finished_courses.append(course)
            self.courses_in_progress.remove(course)
            print(f'\033[34mКурс, {course}, был успешно перемещён в законченные курсы студента {self.name} {self.surname}\033[0m\n') 
        else:
            self.finished_courses.append(course)
            print(f'\033[31mCтудент, {self.name} {self.surname}, ущё не проходил курс {course}\033[0m\n')
            
    def rate_course(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'
    def __str__(self):
        average_grade = average_grade_(self.grades)
        if average_grade == None:
            average_grade = 'Оценок нет'
        finished_courses_str = ', '.join(self.finished_courses)
        if len(finished_courses_str) == 0:
            finished_courses_str = 'Оконченных курсов нет'
        courses_in_progress_str = ', '.join(self.courses_in_progress)
        if len(courses_in_progress_str) == 0:
            courses_in_progress_str = 'Активных курсов нет'
        str_ = f'Имя: \033[31m{self.name}\033[0m\nФамилия: \033[31m{self.surname}\033[0m\nСредняя оценка за лекции: \033[34m{average_grade}\033[0m\nКурсы в процессе изучения: \033[31m{courses_in_progress_str}\033[0m\nЗавершенные курсы: {finished_courses_str}\n'
        return str_
    def __lt__(self, other):
        if not isinstance(other, Student):
            print(f'{other.name} не студент')
            return
        average_grade_(self.grades)
        return average_grade_(self.grades) < average_grade_(other.grades)

class Mentor:
    def __init__(self, name, surname):
        self.name = name.title()
        self.surname = surname.title()
        self.courses_attached = []
    def courses(self, course):
        if course in self.courses_attached:
            print(f'\033[31mПреподователь, {self.name} {self.surname}, уже преподаёт курс {course}\033[0m\n')
        else:
            self.courses_attached += [course]
            print(f'\033[34mКурс, {course}, был успешно добавлен в програму преподователя {self.name} {self.surname}\033[0m\n')
        
class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}
    def __str__(self):
        average_grade = average_grade_(self.grades)
        if average_grade == None:
            average_grade = 'Оценок нет'
        str_ = f'Имя: \033[31m{self.name}\033[0m\nФамилия: \033[31m{self.surname}\033[0m\nСредняя оценка за лекции: \033[34m{average_grade}\033[0m\n'
        return str_
    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            print(f'{other.name} не лектор')
            return
        average_grade_(self.grades)
        return average_grade_(self.grades) < average_grade_(other.grades)

class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return print('Ошибка')
    def __str__(self):
        return f'Имя: \033[31m{self.name}\033[0m\nФамилия: \033[31m{self.surname}\033[0m\n'   



lec1 = Lecturer('namel1', 'surnamel1')
lec2 = Lecturer('namel2', 'surnamel2')
lec3 = Lecturer('namel3', 'surnamel3')
rev1 = Reviewer('namer1', 'surnamer1')
rev2 = Reviewer('namer2', 'surnamer2')
rev3 = Reviewer('namer3', 'surnamer3')
stu1 = Student('names1', 'surnames1', 'm')
stu2 = Student('names2', 'surnames2', 'w')
stu3 = Student('names3', 'surnames3', 'm')
# lec1.courses_attached.append('python')
# rev1.courses_attached.append('python')


stu1.courses('Python')
stu1.courses('Git')
stu1.courses('Введение в програмирование')
stu2.courses('Python')
stu2.courses('Git')
stu2.courses('Введение в програмирование')
lec1.courses('Python')
lec2.courses('Git')
lec3.courses('Введение в програмирование')
rev1.courses('Python')
rev2.courses('Git')
rev3.courses('Введение в програмирование')
# print(stu1.courses_in_progress)
# best_student.courses_in_progress += ['Python']
stu1.end_courses('Введение в програмирование')

rev1.rate_hw(stu1, 'Python', 10)

# print(stu1.grades)
rev1.rate_hw(stu1, 'Python', 9)
rev1.rate_hw(stu2, 'Python', 10)
rev2.rate_hw(stu1, 'Git', 10)
rev1.rate_hw(stu3, 'Python', 9)
rev3.rate_hw(stu1, 'Введение в програмирование', 10)
rev1.rate_hw(stu2, 'Python', 8)
rev2.rate_hw(stu1, 'Git', 9)
rev1.rate_hw(stu3, 'Python', 7)

# print(stu4.grades)
stu1.rate_course(lec1, 'Python', 10)
stu1.rate_course(lec2, 'Git', 10)
stu1.rate_course(lec3, 'Введение в програмирование', 10)
stu2.rate_course(lec1, 'Python', 10)
stu2.rate_course(lec2, 'Git', 9)
stu2.rate_course(lec3, 'Введение в програмирование', 9)
stu3.rate_course(lec1, 'Python', 10)
stu3.rate_course(lec2, 'Git', 9)
stu3.rate_course(lec3, 'Введение в програмирование', 8)

print(lec1)
print(lec2)
print(lec3)
print(rev1)
print(rev2)
print(rev3)
print(stu1)
print(stu2)
print(stu3)

print(lec1 < lec2)
print(stu1 < stu2)

average_grad_curses([stu1, stu2, stu3], 'Python')
average_grad_curses([lec1, lec2, lec3], 'Python')
average_grad_curses([stu1, lec2, stu3], 'Python')
average_grad_curses([stu1, rev2, stu3], 'Python')
