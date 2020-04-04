for f in $(ls | egrep -i '.+\.csv' ); do             
 python plotCSV.py -f $f         
done