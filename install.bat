mkdir D:\cs_tools\scripts\render
curl https://raw.githubusercontent.com/derek640/cs_tools/master/scripts/beauty_ao_shadow_layerManager.py -o D:\cs_tools\scripts\render\
curl https://raw.githubusercontent.com/derek640/cs_tools/master/userSetup.py -o D:\cs_tools\scripts\
for /f "usebackq tokens=2,*" %%A in (`reg query HKCU\Environment /v PYTHONPATH`) do set my_user_pythonpath=%%B
setx PYTHONPATH "D:\cs_tools\;%PYTHONPATH%"