@echo off
REM 定位到磁盘
C:
REM 工作目录------配置项
set WORK_PATH=C:\Users\haichao.zhang\workspace\my_project\test_futu
set Futu_PATH=C:\Users\haichao.zhang\workspace\my_project\futu\FutuOpenD_2.11.850_Windows\FutuOpenD_2.11.850_Windows
REM 配置需要启动的模块----1,表示启动;0,表示不启动
set START_TRADEFRONT=0
set START_QUOTFRONT=1
REM 设置各个目录变量
set DAY=%date:~0,4%%date:~5,2%%date:~8,2%
set MOMENT=%time:~0,6%%time:~6,2%
set logfile=%WORK_PATH%\log\start_work_%DAY%.log
set DAY=%date:~0,4%%date:~5,2%%date:~8,2%
set MOMENT=%time:~0,6%%time:~6,2%
REM 关闭富途网关
taskkill -f -IM FutuOpenD.exe
REM 启动富途网关
cd %Futu_PATH% && start FutuOpenD.exe
ping -n 10 127.0.0.1>nul
REM 判断启动富途网关服务是否成功
tasklist | find /i "FutuOpenD.exe" || (echo FutuOpenD has launched >> %logfile% && echo FutuOpenD not launched !!!)
echo FutuOpenD has launched  >> %logfile% && echo FutuOpenD has launched !!!
echo date:%DAY%,time:%MOMENT%，run >> %logfile%
REM 配置程序路径
cd %WORK_PATH%
venv\Scripts\python run.py
ping -n 10 127.0.0.1>nul
REM 关闭富途网关
taskkill -f -IM FutuOpenD.exe