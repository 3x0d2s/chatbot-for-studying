--
-- Файл сгенерирован с помощью SQLiteStudio v3.2.1 в Сб май 1 12:47:04 2021
--
-- Использованная кодировка текста: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: homework
CREATE TABLE homework (compl_date CHAR (10) NOT NULL, weekday CHAR (16) NOT NULL, lesson CHAR (16) NOT NULL, task CHAR (512) NOT NULL);

-- Таблица: homework_stack
CREATE TABLE homework_stack (user_id CHAR NOT NULL DEFAULT noid, compl_date CHAR (10) NOT NULL, weekday CHAR (16) NOT NULL, lesson CHAR (16) NOT NULL, task CHAR (512) NOT NULL);

-- Таблица: schedule_1
CREATE TABLE schedule_1 (weekday CHAR (15) NOT NULL, start_time CHAR (10) NOT NULL, end_time CHAR (10) NOT NULL, lesson_name CHAR (15) NOT NULL, cabinet CHAR (15) NOT NULL);
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Понедельник', '8:30', '9:15', 'Алгебра', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Понедельник', '9:25', '10:10', 'Физкультура', 'Спортзал');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Понедельник', '10:30', '11:15', 'Русский', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Понедельник', '11:25', '12:10', 'Русский', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Понедельник', '12:30', '13:15', 'Анлийский', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Понедельник', '13:25', '14:10', 'Физика', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Понедельник', '14:20', '15:05', 'Физика', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Вторник', '8:30', '9:15', 'Физпрактика', '23 / 22');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Вторник', '9:25', '10:10', 'Физпрактика', '23 / 22');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Вторник', '10:30', '11:15', 'Геометрия', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Вторник', '11:25', '12:10', 'Геометрия', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Вторник', '12:30', '13:15', 'История', '9');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Вторник', '13:25', '14:10', 'История', '9');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Вторник', '14:20', '15:05', 'Алгебра (Факульт.)', '9');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Среда', '8:00', '9:35', 'Информатика', 'Г-418');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Среда', '9:50', '11:25', 'Английский', 'Д-311');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Среда', '11:55', '13:30', 'Алгебра', 'Д-311');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Четверг', '8:30', '9:15', 'Литература', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Четверг', '9:25', '10:10', 'Литература', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Четверг', '10:30', '11:15', 'Физика', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Четверг', '11:25', '12:10', 'Физика', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Четверг', '12:30', '13:15', 'Геометрия', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Четверг', '13:25', '14:10', 'Инд. проект', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Пятница', '8:30', '9:15', 'Информатика', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Пятница', '9:25', '10:10', 'Информатика', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Пятница', '10:30', '11:15', 'Физика (Лекция)', '23');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Пятница', '11:25', '12:10', 'Физика (Лекция)', '23');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Суббота', '8:30', '9:15', 'История', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Суббота', '9:25', '10:10', 'История', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Суббота', '10:30', '11:15', 'Алгебра', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Суббота', '11:25', '12:10', 'Алгебра', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Суббота', '12:30', '13:15', 'Экономика', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Суббота', '13:25', '14:10', 'Физкультура', 'Спортзал');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Суббота', '14:20', '15:05', 'Астрономия', '22');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Пятница', '12:30', '13:15', 'ОБЖ', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Пятница', '13:25', '14:10', 'Физкультура', 'Спортзал');

-- Таблица: schedule_2
CREATE TABLE schedule_2 (weekday CHAR (15) NOT NULL, start_time CHAR (10) NOT NULL, end_time CHAR (10) NOT NULL, lesson_name CHAR (15) NOT NULL, cabinet CHAR (15) NOT NULL);
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Понедельник', '8:30', '9:15', 'Алгебра', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Понедельник', '9:25', '10:10', 'Физкультура', 'Спортзал');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Понедельник', '10:30', '11:15', 'Русский', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Понедельник', '11:25', '12:10', 'Русский', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Понедельник', '12:30', '13:15', 'Анлийский', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Понедельник', '13:25', '14:10', 'Физика', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Понедельник', '14:20', '15:05', 'Физика', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Вторник', '8:30', '9:15', 'Литература', '20');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Вторник', '9:25', '10:10', 'Литература', '20');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Вторник', '10:30', '11:15', 'Геометрия', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Вторник', '11:25', '12:10', 'Геометрия', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Вторник', '12:30', '13:15', 'Общество', '22');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Вторник', '13:25', '14:10', 'Общество', '22');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Вторник', '14:20', '15:05', 'Алгебра (Факультатив)', '9');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Среда', '8:00', '9:35', 'Информатика', 'Г-418');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Среда', '9:50', '11:25', 'Английский', 'Д-311');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Среда', '11:55', '13:30', 'Алгебра', 'Д-311');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Четверг', '8:30', '9:15', 'Литература', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Четверг', '9:25', '10:10', 'Литература', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Четверг', '10:30', '11:15', 'Физика', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Четверг', '11:25', '12:10', 'Физика', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Четверг', '12:30', '13:15', 'Геометрия', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Четверг', '13:25', '14:10', 'Инд. проект', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Пятница', '8:30', '9:15', 'Информатика', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Пятница', '9:25', '10:10', 'Информатика', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Пятница', '10:30', '11:15', 'Физика (Лекция)', '23');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Пятница', '11:25', '12:10', 'Физика (Лекция)', '23');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Суббота', '8:30', '9:15', 'Общество', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Суббота', '9:25', '10:10', 'Общество', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Суббота', '10:30', '11:15', 'Алгебра', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Суббота', '11:25', '12:10', 'Алгебра', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Суббота', '12:30', '13:15', 'Экономика', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Суббота', '13:25', '14:10', 'Физкультура', 'Спортзал');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Суббота', '14:20', '15:05', 'Астрономия', '22');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Пятница', '12:30', '13:15', 'ОБЖ', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Пятница', '13:25', '14:10', 'Физкультура', 'Спортзал');

-- Таблица: users
CREATE TABLE "users" (
	"user_id"	INTEGER NOT NULL UNIQUE,
	"isAdmin"	BOOLEAN NOT NULL DEFAULT (False),
	"homework_f"	BOOLEAN NOT NULL DEFAULT (False),
	"schedule_f"	BOOLEAN NOT NULL DEFAULT (False),
	"addHomew_f"	BOOLEAN NOT NULL DEFAULT (False),
	"delHome_f"	BOOLEAN NOT NULL DEFAULT (False),
	"getLessDate_f"	BOOLEAN NOT NULL DEFAULT (False),
	"step_code"	INTEGER NOT NULL DEFAULT (0),
	"editHomew_f"	BOOLEAN NOT NULL DEFAULT (False)
);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
