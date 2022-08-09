mkdir failures
find . -maxdepth 1 -name "*.tar.gz" -size $1 -exec mv {} failures/ \; 
