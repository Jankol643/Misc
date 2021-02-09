#!/bin/bash
<< 'MULTILINE-COMMENT'
    This program reads a filename from STDIN and cleans the file
    Usage cleaner.sh filename.txt
    Date 5/2/2021
    Author Jan Kolnberger
    Dependencies: bc for calculation, time for measuring execution time
MULTILINE-COMMENT

filename=$1 # read file name from command line as argument
output="final" #  file name of output file
# https://stackoverflow.com/questions/64257286/giving-a-bash-script-the-option-to-accepts-flags-like-a-command/64257864#64257864
# https://medium.com/@Drew_Stokes/bash-argument-parsing-54f3b81a6a8f

# Ask user if command should be timed
read -p "Should the command be timed? [y/n]" timed
if [[ $timed==[yY] ]]; then
    echo "Command will be timed."
    /bin/time -v cleaner.sh #measures script execution time more precisely than with built-in time
else
    echo "Not timing command."
fi

# print general information about the file
echo "filename" $1 # prints the filename
nolines=$(wc -l < $1) # saves the no. of lines in a variable
echo "no. of lines" $nolines # prints the number of lines
nowords=$(wc -w < $1) # saves the no. of lines in a variable

echo "sort by no. of occurences"
sort -n $1 > ${1}_occur.txt # sort by no. of occurences
echo "remove duplicates"
awk '!visited[$0]++' ${1}_occur.txt > $output # remove duplicates, https://iridakos.com/programming/2019/05/16/remove-duplicate-lines-preserving-order-linux

rm ${1}_occur.txt # delete temporary file

# prop=$(echo "scale=2;$nolines2/$nolines" | bc) # https://stackoverflow.com/questions/12722095/how-do-i-use-floating-point-division-in-bash
# echo "proportion of unique lines" $prop

# calculating file sizes
finalbc=$(wc -c < $output) # filesize in bytes
sizeMB=$(bc <<< "scale=2 ; $finalbc / 1024") # filesize in MB
sizeGB=$(bc <<< "scale=2 ; $finalbc / 1024^2") # filesize in GB
echo "Filesize: " $sizeMB "MB, " $sizeGB "GB"

finalwords=$(wc -w $output) #words in final file
echo "Words in final file: " $finalwords
duplicates=$nowords-$finalwords
dupepercentage=$(bc <<< "scale=2 ; $duplicates / $nowords")
echo "duplicates: " $duplicates ", " "duplicated percentage: " $dupepercentage

echo "Script finished successfully. Outputfile: " $output

# Ask user if generated file should be analysed using PACK
read -p "PACK analysis [y/n]" PACK_decis
if [[ $PACK_decis==[yY] ]]; then
    echo "Feeding the file to PACK for analysis"
    statsgen $output -o passwords_masks$output # feed the file to PACK for analysis
else
    echo "Not analysing file. "
    echo "Exiting script..."
    exit 1 # terminate the script
fi