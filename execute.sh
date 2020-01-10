curl https://caixapreta.pt/listas/guide.xml.gz  --output guide.xml.gz
rm -rf guide.xml
gunzip guide.xml.gz
sh replace.sh &
