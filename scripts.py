from datacenter.models import *
import random
from datetime import datetime


COMMENDATIONS = ('Отличный ответ!', 'Молодец!', 'Замечательно')


def fix_marks(schoolkid):
    Mark.objects.filter(schoolkid=schoolkid, points__in=[2,3]).update(points=5)


def remove_chastisements(schoolkid):
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def create_commendation(schoolkid, subject_title): 
    group_letter = schoolkid.group_letter
    year_of_study = schoolkid.year_of_study
    while True:
        try:
            date_input = input('Введите дату (день.месяц.год): ')
            lesson_date = datetime.strptime(date_input, '%d-%m-%Y')
            break
        except:
            print('Неверная дата')
    lessons = Lesson.objects.filter(
        group_letter=group_letter, year_of_study=year_of_study,
        subject__title=subject_title, date=lesson_date
        ).order_by('date')
    lessons_count = lessons.count()
    if lessons_count > 1:
        for i, lesson in enumerate(lessons, 1):
            lesson_time = lesson.TIMESLOTS_SCHEDULE[lesson.timeslot - 1]
            print(f'Урок {i}. Преподаватель: {lesson.teacher}, класс: {lesson.room}, время: {lesson_time}')
        while True:
            try: 
                lesson_number_input =  input('Введите номер урока: ')
                lesson = lessons[int(lesson_number_input) - 1]
                break
            except:
                print('Неверный номер урока')
    elif lessons_count == 1:
        lesson = lessons.first()
    else: 
        raise Exception('Уроки не найдены') 
    
    Commendation.objects.create(
        text=random.choice(COMMENDATIONS), created=lesson.date,schoolkid=schoolkid,
        subject=lesson.subject, teacher=lesson.teacher
        )


def main():
    while True:
        try:
            schoolkid_name = input('Введите ФИО ученика: ')
            schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
            break
        except Schoolkid.MultipleObjectsReturned:
            print('Есть несколько учеников с такими данными')
        except Schoolkid.DoesNotExist:
            print('Ученик не найден')

    fix_marks(schoolkid)

    remove_chastisements(schoolkid)

    while True:
        try:
            subject_title = input('Введите название предмета: ')
            create_commendation(schoolkid, subject_title)
            break
        except Exception:
            print('Уроки не найдены')
    
    print('Скрипт завершил работу')


if __name__ == '__main__':
    main()
    