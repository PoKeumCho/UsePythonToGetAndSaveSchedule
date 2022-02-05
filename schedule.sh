#!/bin/bash

if (( $1 > 2010 ))
then
    if [[ $2 == 1학기 || $2 == 여름계절학기 || $2 == 2학기 || $2 == 겨울계절학기 ]]
    then
        echo 기존의 데이터를 모두 삭제한다.
        rm ./log/* ./pickle/* ./txt/*

        cd ./python

        python schedule.py $1 $2 교양
        python schedule_file_analysis.py 교양

        python schedule.py $1 $2 전공
        python schedule_file_analysis.py 전공

        python schedule.py $1 $2 교직
        python schedule_file_analysis.py 교직

        python schedule.py $1 $2 사이버
        python schedule_file_analysis.py 사이버
    else
        echo 학기 정보가 올바르지 않습니다.
    fi
else
    echo 학년도 정보가 올바르지 않습니다.
fi
