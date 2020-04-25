for f in $(ls $1 | egrep -i '.+\.csv' ); do             
 python plotCSV.py -f $1/$f         
done