source env/bin/activate
nohup ./manage.py runserver 0.0.0.0:80 > my.log 2>&1 &
echo $! > save_pid.txt
