import mariadb
import sys
import pickle

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="put_user_here",
        password="put_pw_here",
        host="localhost",
        port=3306,
        database="put_db_here"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

# schedule 테이블을 생성한다.
try:
    cur.execute('DROP TABLE IF EXISTS `scheduletbl`')
    cur.execute('''
        CREATE TABLE `scheduletbl` (
            `no`            SMALLINT AUTO_INCREMENT NOT NULL PRIMARY KEY,   -- 고유번호(PK)
            `subjects`      VARCHAR(3),                                     -- 과목구분
            `department`    VARCHAR(20),                                    -- 개설학과전공
            `classNumber`   VARCHAR(10),                                    -- 학수번호
            `className`     VARCHAR(80) NOT NULL,                           -- 교과목명
            `bunban`        CHAR(3) NOT NULL,                               -- 분반
            `isugubun`      VARCHAR(4),                                     -- 이수구분
            `classTime`     VARCHAR(80) NOT NULL,                           -- 시간표
            `campus`        CHAR(2) NOT NULL,                               -- 캠퍼스
            `roomAndProf`   VARCHAR(50)                                     -- 강의실/담당교수
        )
            ''')
except mariadb.Error as e: 
    print(f"Error [CREATE TABLE]: {e}")


# 데이터를 저장한다.
try:
    with open('../pickle/schedule.pickle', 'rb') as fp:
        schedules = pickle.load(fp)
        for schedule in schedules:
            cur.execute('''
                INSERT INTO `scheduletbl` 
                    VALUES (NULL, %(subjects)s, %(department)s, %(classNumber)s, %(className)s, 
                            %(bunban)s, %(isugubun)s, %(classTime)s, %(campus)s, %(roomAndProf)s)
                    ''', schedule)
except mariadb.Error as e:    
    print(f"Error [INSERT]: {e}")


# 이전 시간표 관련 테이블을 초기화한다.
try:
    #cur.execute('TRUNCATE TABLE `userscheduletbl`')
    cur.execute('TRUNCATE TABLE `schedulelookuptbl`')
except mariadb.Error as e: 
    print(f"Error [TRUNCATE TABLE]: {e}")


# 변경사항을 저장한다.
conn.commit()

conn.close()
