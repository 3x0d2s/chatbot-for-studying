--
-- Файл сгенерирован с помощью SQLiteStudio v3.2.1 в Чт июн 10 23:45:08 2021
--
-- Использованная кодировка текста: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: homework
CREATE TABLE IF NOT EXISTS homework (compl_date CHAR (10) NOT NULL, weekday CHAR (16) NOT NULL, lesson CHAR (16) NOT NULL, task CHAR (512) NOT NULL);

-- Таблица: homework_f_tomorrow
CREATE TABLE IF NOT EXISTS homework_f_tomorrow (user_id INTEGER UNIQUE NOT NULL);

-- Таблица: homework_stack
CREATE TABLE IF NOT EXISTS homework_stack (user_id CHAR NOT NULL DEFAULT noid, compl_date CHAR (10) NOT NULL, weekday CHAR (16) NOT NULL, lesson CHAR (16) NOT NULL, task CHAR (512) NOT NULL);

-- Таблица: schedule_1
CREATE TABLE IF NOT EXISTS schedule_1 (weekday CHAR (15) NOT NULL, start_time CHAR (10) NOT NULL, end_time CHAR (10) NOT NULL, lesson_name CHAR (15) NOT NULL, cabinet CHAR (15) NOT NULL);
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Понедельник', '8:30', '9:15', 'Русский', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Понедельник', '9:25', '10:10', 'Русский', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Понедельник', '10:30', '11:15', 'Общество', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Понедельник', '11:25', '12:10', 'История', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Понедельник', '12:30', '13:15', 'Алгебра', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Понедельник', '13:25', '14:10', 'Алгебра', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Понедельник', '14:20', '15:05', 'Физкультура', 'Спортзал');
--
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Вторник', '8:30', '9:15', 'Физика', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Вторник', '9:25', '10:10', 'Физика', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Вторник', '10:30', '11:15', 'Геометрия', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Вторник', '11:25', '12:10', 'Литература', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Вторник', '12:30', '13:15', 'Литература', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Вторник', '13:25', '14:10', 'Инд. проект', '18');
--
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Среда', '8:00', '9:35', 'Алгебра', 'Д-311');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Среда', '9:50', '11:25', 'Англ./Инф.', 'Д-314/Г-418');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Среда', '11:55', '13:30', 'Англ./Инф.', 'Д-314/Г-418');
--
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Четверг', '8:30', '9:15', 'Физ. практика', '22/23');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Четверг', '9:25', '10:10', 'Литература', '35');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Четверг', '10:30', '11:15', 'Физкультура', 'Спортзал');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Четверг', '11:25', '12:10', 'Английский', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Четверг', '12:30', '13:15', 'Алгебра', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Четверг', '13:25', '14:10', 'Физика', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Четверг', '14:20', '15:05', 'Физика', '18');
--
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Пятница', '8:30', '9:15', 'Информатика', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Пятница', '9:25', '10:10', 'Информатика', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Пятница', '10:30', '11:15', 'История', '22');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Пятница', '11:25', '12:10', 'Общество', '22');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Пятница', '12:30', '13:15', 'Физика (лекция)', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Пятница', '13:25', '14:10', 'Физика (лекция)', '18');
--
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Суббота', '8:30', '9:15', 'ЭК РЭЗ', '18');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Суббота', '9:25', '10:10', 'Физкультура', 'Спортзал');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Суббота', '10:30', '11:15', 'ЭК БиоХ', '9');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Суббота', '11:25', '12:10', 'ОБЖ', '22');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Суббота', '12:30', '13:15', 'Геометрия', '16');
INSERT INTO schedule_1 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Суббота', '13:25', '14:10', 'Геометрия', '16');
--


-- Таблица: schedule_2
CREATE TABLE IF NOT EXISTS schedule_2 (weekday CHAR (15) NOT NULL, start_time CHAR (10) NOT NULL, end_time CHAR (10) NOT NULL, lesson_name CHAR (15) NOT NULL, cabinet CHAR (15) NOT NULL);
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Понедельник', '8:30', '9:15', 'Русский', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Понедельник', '9:25', '10:10', 'Русский', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Понедельник', '10:30', '11:15', 'Общество', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Понедельник', '11:25', '12:10', 'История', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Понедельник', '12:30', '13:15', 'Алгебра', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Понедельник', '13:25', '14:10', 'Алгебра', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Понедельник', '14:20', '15:05', 'Физкультура', 'Спортзал');
--
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Вторник', '8:30', '9:15', 'Физика', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Вторник', '9:25', '10:10', 'Физика', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Вторник', '10:30', '11:15', 'Геометрия', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Вторник', '11:25', '12:10', 'Литература', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Вторник', '12:30', '13:15', 'Литература', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Вторник', '13:25', '14:10', 'Инд. проект', '18');
--
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Среда', '8:00', '9:35', 'Алгебра', 'Д-311');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Среда', '9:50', '11:25', 'Англ./Инф.', 'Д-314/Г-418');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Среда', '11:55', '13:30', 'Англ./Инф.', 'Д-314/Г-418');
--
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Четверг', '8:30', '9:15', 'Физ. практика', '22/23');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Четверг', '9:25', '10:10', 'Литература', '35');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Четверг', '10:30', '11:15', 'Физкультура', 'Спортзал');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Четверг', '11:25', '12:10', 'Английский', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Четверг', '12:30', '13:15', 'Алгебра', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Четверг', '13:25', '14:10', 'Физика', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Четверг', '14:20', '15:05', 'Физика', '18');
--
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Пятница', '8:30', '9:15', 'Информатика', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Пятница', '9:25', '10:10', 'Информатика', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Пятница', '10:30', '11:15', 'История', '22');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Пятница', '11:25', '12:10', 'Общество', '22');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Пятница', '12:30', '13:15', 'Физика (лекция)', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Пятница', '13:25', '14:10', 'Физика (лекция)', '18');
--
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Суббота', '8:30', '9:15', 'ЭК РЭЗ', '18');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Суббота', '9:25', '10:10', 'Физкультура', 'Спортзал');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Суббота', '10:30', '11:15', 'ЭК БиоХ', '9');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Суббота', '11:25', '12:10', 'ОБЖ', '22');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Суббота', '12:30', '13:15', 'Геометрия', '16');
INSERT INTO schedule_2 (weekday, start_time, end_time, lesson_name, cabinet) VALUES ('Суббота', '13:25', '14:10', 'Геометрия', '16');
--

-- Таблица: users
CREATE TABLE IF NOT EXISTS "users" (
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
-- можно раскомментировать строку снизу и вписать ID аккаунта вместо 7777777, тем самым сделать нужный аккаунт администратором сразу
-- INSERT INTO users (user_id, isAdmin, homework_f, schedule_f, addHomew_f, delHome_f, getLessDate_f, step_code, editHomew_f) VALUES (7777777, 1, 0, 0, 0, 0, 0, 0, 0);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
