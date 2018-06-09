@echo off
setlocal enabledelayedexpansion
for %%j in (*.*) do (
set filename=%%~nj
set filename=!filename:_=!
set filename=!filename: =!
if not "!filename!"=="%%~nj" ren "%%j" "!filename!%%~xj"
)