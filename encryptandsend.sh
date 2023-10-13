backupFolder=""
zipLocation=""

rm encryptandsendinfo.txt
password=`tr -dc A-Za-z0-9 </dev/urandom | head -c 64 ; echo ''`
7za a -tzip -p$password -mem=AES256 $zipLocation -r $backupFolder
chmod 777 $zipLocation
sha256Hash=`sha256sum $zipLocation | awk '{ print $1 }'`
downloadUrl=`curl -F file=@$zipLocation https://store1.gofile.io/uploadFile -s | awk -F '"' '{print $14}'`
fileSize=`du -sh $zipLocation | awk '{ print $1 }'`

echo $password > encryptandsendinfo.txt
echo $downloadUrl >> encryptandsendinfo.txt
echo $sha256Hash >> encryptandsendinfo.txt
echo $fileSize >> encryptandsendinfo.txt