@echo off
REM ��λ������
C:
REM ����Ŀ¼------������
set WORK_PATH=C:\Users\haichao.zhang\workspace\my_project\test_futu
set Futu_PATH=C:\Users\haichao.zhang\workspace\my_project\futu\FutuOpenD_2.11.850_Windows\FutuOpenD_2.11.850_Windows
REM ������Ҫ������ģ��----1,��ʾ����;0,��ʾ������
set START_TRADEFRONT=0
set START_QUOTFRONT=1
REM ���ø���Ŀ¼����
set DAY=%date:~0,4%%date:~5,2%%date:~8,2%
set MOMENT=%time:~0,6%%time:~6,2%
set logfile=%WORK_PATH%\log\start_work_%DAY%.log
set DAY=%date:~0,4%%date:~5,2%%date:~8,2%
set MOMENT=%time:~0,6%%time:~6,2%
REM �رո�;����
taskkill -f -IM FutuOpenD.exe
REM ������;����
cd %Futu_PATH% && start FutuOpenD.exe
ping -n 10 127.0.0.1>nul
REM �ж�������;���ط����Ƿ�ɹ�
tasklist | find /i "FutuOpenD.exe" || (echo FutuOpenD has launched >> %logfile% && echo FutuOpenD not launched !!!)
echo FutuOpenD has launched  >> %logfile% && echo FutuOpenD has launched !!!
echo date:%DAY%,time:%MOMENT%��run >> %logfile%
REM ���ó���·��
cd %WORK_PATH%
venv\Scripts\python run.py
ping -n 10 127.0.0.1>nul
REM �رո�;����
taskkill -f -IM FutuOpenD.exe