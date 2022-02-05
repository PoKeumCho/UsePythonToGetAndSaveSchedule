import mariadb
import sys

# 쉘에서 python filename.py (요일) 형태로 호출한다.
if len(sys.argv) != 2:
    print('ERROR: Wrong Format', file=sys.stderr)
    raise Exception

# 요일 (월, 화, 수, 목, 금)
DAY_OF_WEEK = sys.argv[1] 

result = list()

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

try:
    cur.execute('SELECT `no`, `classTime` FROM `scheduletbl` WHERE `classTime` LIKE ?', 
            ('%' + DAY_OF_WEEK + '%',))

    for (no, classTime) in cur:

        # '월/7-8,화/3' 형태로 구성된다는 점에 유의한다.
        # (해당 요일)/(숫자) 부분 추출
        classTimeList = classTime.split(',')
        for i in range(len(classTimeList)):
            if (classTimeList[i][0] == DAY_OF_WEEK):
                classTime = classTimeList[i]
                break
        # (숫자) 부분만 저장한다.
        classTime = classTime.split('/')[1]

        # 튜플 형태의 (no, 교시)를 result 리스트에 저장한다. 
        classTimeList = classTime.split('-')
        if (len(classTimeList) == 1):
            result.append((no, int(classTimeList[0])))
        elif (len(classTimeList) == 2):
            for i in range(int(classTimeList[0]), int(classTimeList[1]) + 1):
                result.append((no, i))

except mariadb.Error as e: 
    print(f"Error [SELECT / APPEND TO RESULT]: {e}")


tableNameDict = {
        '월': 'montbl', 
        '화': 'tuetbl', 
        '수': 'wedtbl', 
        '목': 'thutbl', 
        '금': 'fritbl'
        }

# schedule 룩업 테이블을 생성한다.
try:
    cur.execute('DROP TABLE IF EXISTS `' + tableNameDict[DAY_OF_WEEK] + '`')
    cur.execute('''
        CREATE TABLE `''' +  tableNameDict[DAY_OF_WEEK] + '''` (
            `no`            SMALLINT NOT NULL,
            `classTime`     TINYINT,
            PRIMARY KEY(`no`, `classTime`)
        )
        ''')
except mariadb.Error as e: 
    print(f"Error [CREATE TABLE]: {e}")


# 데이터를 저장한다.
try:
    for i in range(len(result)):
        no, classTime = result[i]   # 튜플 언팩
        cur.execute('INSERT INTO `' + tableNameDict[DAY_OF_WEEK] + '` VALUES (?, ?)', 
                (no, classTime))
except mariadb.Error as e:    
    print(f"Error [INSERT]: {e}")

# 변경사항을 저장한다.
conn.commit()

conn.close()
