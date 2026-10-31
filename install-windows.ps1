$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
python maet.py install $args
python maet.py doctor
