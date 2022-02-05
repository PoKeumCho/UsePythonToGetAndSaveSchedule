import re
import sys
import pickle

# 쉘에서 python filename.py SUBJECTS 형태로 호출한다.    
if len(sys.argv) != 2:    
    print('ERROR: Wrong Format', file=sys.stderr)    
    raise Exception    

SUBJECTS = (sys.argv[1])    

# 전체 결과를 저장하는 schedules 리스트를 불러온다.
try:
    with open('../pickle/schedule.pickle', 'rb') as f:
        schedules = pickle.load(f)
except FileNotFoundError:
    schedules = []

#=================================================================================================================#
#   ['No', '개설학과전공', '학수번호', '교과목명', '분반', '이수구분', '시간표', '캠퍼스', '강의실/담당교수']
#=================================================================================================================#


with open('../txt/schedule.txt', 'rt') as f,\
        open('../log/schedule_file_analysis.debug.txt', 'at') as debug,\
        open('../log/schedule_file_analysis.result.txt', 'at') as result:

    print('{:=^100}'.format(SUBJECTS), file=debug)
    print('{:=^100}'.format(SUBJECTS), file=result)


    for line in f:

        # 데이터가 없는 경우
        if line == '\n':
            print('데이터가 존재하지 않습니다.', file=sys.stderr)
            break

        #==============================================================================================#
        #   'No', '개설학과전공', '학수번호', '교과목명', '분반', '이수구분' 은 공통적으로 존재하므로 
        #   해당 값들을 먼저 추출한다. 
        #==============================================================================================#

        # '교과목명'에는 빈 문자열이 포함되어 있으므로 먼저 ['No', '개설학과전공', '학수번호' , '그 외']로 나눈다.
        schedule = line.split(maxsplit=3)

        # schedule 리스트의 '그 외' 요소를 리스트에서 삭제 후 else_str에 저장한다.
        else_str = schedule.pop()
       
        # '분반' 형식과 일치하는 정규 표현식을 검색한다.
        bunban = re.search(r'[0-9]{3}', else_str)
        if bunban:
            bunban_pos = bunban.span()

            # '분반' 이전에 위치하는 '교과목명'을 schedule 리스트에 추가한다.
            schedule.append(else_str[:bunban_pos[0]-1])
            # '분반'을 schedule 리스트에 추가한다.
            schedule.append(bunban.group(0))
            # 리스트에 추가된 내용을 문자열에서 삭제한다.
            else_str = else_str[bunban_pos[1]+1:]

            # '이수구분'을 schedule 리스트에 추가하고, 추가된 내용은 문자열에서 삭제한다.
            temp_list = else_str.split(maxsplit=1)
            schedule.append(temp_list[0])
            else_str = temp_list[1]
        else:
            print(schedule
                    , ": '분반' 형식과 일치하는 정규 표현식 검색에 실패하여 해당 데이터는 처리하지 않습니다."
                    ,file=sys.stderr)
            continue
            

        # 추출된 중간값 확인용
        print(schedule, file=debug)
        print(else_str, file=debug)

        #==============================================================================================#
        #   '시간표', '강의실', '담당교수', '캠퍼스' 정보를 추가로 추출한다.
        #   해당 내용이 없는 경우에는 빈 문자열을 집어넣는다.
        #==============================================================================================#
        
        # '시간표' 항목은 반드시 존재해야 한다. 
        # '시간표' 항목이 존재하는 경우 schedule 리스트에 추가하고, 그 앞의 내용들은 문자열에서 삭제한다.
        period = re.search(r'([월화수목금토일]/(\S*))\s', else_str)
        if period :
            schedule.append(period.group(1))
            period_pos = period.span()
            else_str = else_str[period_pos[1]:]
        else:
            print(schedule
                    , ": '시간표' 형식과 일치하는 정규 표현식 검색에 실패하여 해당 데이터는 처리하지 않습니다."
                    ,file=sys.stderr)
            continue
                    
        # 추출된 중간값 확인용
        print(schedule, file=debug)
        print(else_str, file=debug)

        # '캠퍼스' 항목은 공통적으로 존재하므로 먼저 추출한다.
        campus = re.search(r'(수정|운정|공용)', else_str)
        if campus:
            schedule.append(campus.group(0))
            campus_pos = campus.span()

            # '강의실', '담당교수' 항목이 존재하지 않으면 더 이상 추출할 항목이 없다.
            if campus_pos[0] == 0:
                else_str = ''
            else:
                else_str = else_str[:campus_pos[0]-1]

        else:
            print(schedule
                    , ": '캠퍼스' 형식과 일치하는 정규 표현식 검색에 실패하여 해당 데이터는 처리하지 않습니다."
                    ,file=sys.stderr)
            continue

        # 남은 '강의실/담당교수' 항목을 schedule 리스트에 추가한다.
        schedule.append(else_str)

        # 추출된 중간값 확인용
        print(schedule, file=debug)
        print(else_str, file=debug)
        print('-' * 100, file=debug)

        # 추출된 결과값 확인용
        print(schedule, file=result)

        # 전체 결과를 저장하는 schedules 리스트에 데이터를 추가한다.
        schedules.append({ 
            'subjects': SUBJECTS,           # 과목구분
            'no': schedule[0],              # No
            'department': schedule[1],      # 개설학과전공
            'classNumber': schedule[2],     # 학수번호
            'className': schedule[3],       # 교과목명
            'bunban': schedule[4],          # 분반
            'isugubun': schedule[5],        # 이수구분
            'classTime': schedule[6],       # 시간표
            'campus': schedule[7],          # 캠퍼스
            'roomAndProf': schedule[8]      # 강의실/담당교수
            })


with open('../pickle/schedule.pickle', 'wb') as f:
    pickle.dump(schedules, f)
