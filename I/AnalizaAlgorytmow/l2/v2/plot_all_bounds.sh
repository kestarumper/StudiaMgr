for f in $(ls $1 | egrep -i '.+?\.csv' ); do             
 python zad7.py -f $1/$f -a 0.005
 python zad7.py -f $1/$f -a 0.01
 python zad7.py -f $1/$f -a 0.05
done