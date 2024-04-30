@echo on
cd C:\Users\Mindtrap\Downloads\usbmmidd_v2\usbmmidd_v2
timeout 1 > NUL
start cmd.exe /c "deviceinstaller64 enableidd 1"
timeout 5 > NUL
@echo "Finished"