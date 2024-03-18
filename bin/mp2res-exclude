#!/bin/bash

restar=$1

files_to_check=(
    "mp-1209929-GGA+U.res"      
    "mp-1014111-GGA.res"        
    "mp-1094136-GGA.res"        
    "mp-1213623-GGA+U.res"   
)

for file in "${files_to_check[@]}"; do
    # Check if the file exists in the tar archive
    if tar -tf "$restar" | grep -q "^$file$"; then
        tar --delete -f "$restar" "$file"
        echo "File $file deleted."
    fi
done
