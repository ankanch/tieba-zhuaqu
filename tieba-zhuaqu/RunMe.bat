@echo off
@echo      该python脚本可以用于抓取贴吧帖子数据（标题，作者，发帖时间）    
@echo           请确认你已经安装python3.5及以上版本             
@echo            by Kanch kanchisme@gmail.com               
@echo -
@echo -
@echo -
reg query "HKEY_CURRENT_USER\SOFTWARE\Python\PythonCore\3.5"  
if ERRORLEVEL 1 GOTO NOPYTHON  
goto :HASPYTHON  
:NOPYTHON  
@echo      未检测到python3.5，将自动安装...
pause
\pyIns\python-3.5.2.exe
:HASPYTHON  
@echo      检测到Python3.5脚本可以继续执行
@echo -
@echo -
@echo -
pause 
python main.py