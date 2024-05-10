echo 79583390-9c93-11ed | "C:\Program Files (x86)\AnyDesk\anydesk.exe" --set-password "_unattended_access"
@echo on
timeout 1 > NUL
del "C:\ProgramData\AnyDesk\service.conf"
timeout 5 > NUL
taskkill /F /IM "AnyDesk.exe" /T
timeout 5 > NUL
start "" "C:\Program Files (x86)\AnyDesk\anydesk.exe" --start
timeout 8 > NUL
echo mindtr@p | "C:\Program Files (x86)\AnyDesk\anydesk.exe" --set-password "_unattended_access"
timeout 5 > NUL
echo "Succesfully updated Anydesk-ID and set _unattended_access for the current profile"
timeout 5 > NUL