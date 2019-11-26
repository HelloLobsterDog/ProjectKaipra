@echo off

rmdir .\build /S /Q
rmdir .\dist /S /Q
rmdir .\logs /S /Q
rmdir .\dirt\__pycache__ /S /Q
rmdir .\dirt\action_effects\__pycache__ /S /Q
rmdir .\dirt\template_actions\__pycache__ /S /Q
rmdir .\tests\__pycache__ /S /Q

del .\MANIFEST
