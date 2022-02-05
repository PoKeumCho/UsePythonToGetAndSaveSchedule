import pickle
import json

json_data = {}

with open('../pickle/schedule.pickle', 'rb') as fp,\
        open('../json/schedule.json', 'w') as fj:
            
            schedules = pickle.load(fp)

            # schedule은 아래의 키를 갖는 딕셔너리 형태이다.
            # 키 : subjects, department,classNumber, className, bunban, 
            #       isugubun, classTime, campus, roomAndProf
            for schedule in schedules:
                # json_schedules은 리스트 형태이다.
                json_schedules = json_data.setdefault(schedule['subjects'], []) 
                schedule.pop('subjects')
                json_schedules.append(schedule)
                

            json.dump(json_data, fj, ensure_ascii=False, indent=4)    
