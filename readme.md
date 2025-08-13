Instructions on how to run the website on your local computer

if you dont have git bash in you computer download it by
https://git-scm.com/downloads


clone the repository https://github.com/Alifaeenali/mindtune

open command prompt and clone repository in your preffered folder by running: 

cd path/to/yourFolder
git clone https://github.com/Alifaeenali/mindtune

To check if your pc has python installed run this command on your pc: 
python --version

if python is not avaliable please watch this video for a successfull installation of python in your computer: 

https://www.youtube.com/watch?v=NfTrFhfqmFY

Next install mysql server in your computer:
go to this link: 
https://dev.mysql.com/downloads/installer/

click on download on file with lower memory ~2-3M and then on 'no thanks, just start my download.'

click the downloaded file, and select server only , press next then press execute

after completion press next and then again execute, then next , next next, next, then set a password and save it in some place, next , next, next and then execute, 
after message of successful configuration on bottom, press finish
in product configuration press next then finish

open the folder 

run this in cmd/terminal

pip install -r requirement.txt

after that open .env file and set your own credidentials there

for email first turn on two step authentication you want to send email through , then get a app password from chrome by searching

app password for gmail

once password created you can update gmail password in .env file and gmail too. 

then run on terminal/cmd

#to setup database
python setupdb.py

#to run server
python app.py

the link will show up in the terminal

copy paste that link in browser or ctrl+click on that link