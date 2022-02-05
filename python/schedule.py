import time
import sys
from selenium import webdriver

# 쉘에서 python filename.py YEAR SEMESTER SUBJECTS 형태로 호출한다.
if len(sys.argv) != 4:
    print('ERROR: Wrong Format', file=sys.stderr)
    raise Exception

YEAR = int(sys.argv[1])
SEMESTER = sys.argv[2]
SUBJECTS = sys.argv[3]

# firefox 모듈의 WebDriver 객체를 생성한다.
driver = webdriver.Firefox()

def main():
    # 수강 신청 시스템 페이지를 연다.
    print('Accessing to View All Courses page ...', file=sys.stderr)
    driver.get('https://sugang.sungshin.ac.kr/timetable.do?orgClsfCd=COMM075.101')

    # 로그인 페이지에 들어가졌는지 확인한다.
    # title 요소의 텍스트가 일치하지 않으면 AssertionError 예외가 발생한다.
    assert '수강신청 시스템' in driver.title

    # 첫 번째 iframe 안으로 이동하기
    # time.sleep을 추가하지 않은 경우, NoSuchElementException: Message: Unable to locate element 에러가 발생한다.
    time.sleep(2)
    pop_up = driver.find_element_by_id('contentsFrm')
    driver.switch_to.frame(pop_up)
    time.sleep(2)

    #========================= 학년도 지정 =========================#
    input_year = driver.find_element_by_id('ipbYy')
    # input 태그의 기본 값을 가져온다.
    current_year = int(input_year.get_attribute('value'))
    if YEAR > current_year:
        print('Not Available Year: ' + str(YEAR), file=sys.stderr)
    elif YEAR == current_year:
        print('(Most Recent Year) Set Year: ' + str(YEAR), file=sys.stderr)
    else:
        # input 태그의 기본 값을 지우고 새로운 값을 넣는다.
        input_year.clear()
        input_year.send_keys(YEAR)
        print('Set Year: ' + str(YEAR), file=sys.stderr)


    #========================== 학기 지정 ==========================#
    select_semester = driver.find_element_by_id('cmbSemCd')
    driver.execute_script('var select = arguments[0];' + 
            'for(var i = 0; i < select.options.length; i++) {' +
            '   if(select.options[i].text == arguments[1]){' + 
                    'select.options[i].selected = true; } }'
                    ,select_semester, SEMESTER)
    print('Set Semester: ' + SEMESTER, file=sys.stderr)


    #========================= 과목구분 지정 =========================#
    select_subjects = driver.find_element_by_id('cmbSbjMngCd')
    driver.execute_script('var select = arguments[0];' + 
            'for(var i = 0; i < select.options.length; i++) {' +
            '   if(select.options[i].text == arguments[1]){' + 
                    'select.options[i].selected = true; } }'
                    ,select_subjects, SUBJECTS)
    print('Set Subjects: ' + SUBJECTS, file=sys.stderr)


    # 개설강좌를 조회한다. 
    driver.find_element_by_id('btnSch').click()
    # 바로 로드되지 않으므로 약간의 시간 간격을 둔다.
    time.sleep(2)

    # 조회된 개설강좌를 txt/schedule.txt에 출력한다.
    with open('../txt/schedule.txt', 'wt') as f:
        for schedule_table in driver.find_elements_by_css_selector('#divGrxMst > #grxMst > tbody'):
            print(schedule_table.text, file=f)

    # closes current window on which Selenium is running automated tests.
    driver.close()
    

main()
