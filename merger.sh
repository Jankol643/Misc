#!/bin/bash
<< 'MULTILINE-COMMENT'
    This program merges and deduplicates all files in a folder
    Usage cleaner.sh
    Date 5/2/2021
    Author Jan Kolnberger
    Dependencies: time (for measuring execution time), wc (for counting words and file sizes), rm (for removing files), bc (for calculating)
MULTILINE-COMMENT

# filepath=$1 # read file name from command line as argument
# read -p "Enter path: " $filepath # prompt the user to enter a filepath
filepath=./test1/
output="final" #  file name of output file
output=$filepath_$output

# Ask user if command should be timed
read -p "Should the command be timed? [y/n]" timed
if [[ $timed==[yY] ]]; then
    echo "Command will be timed."
    /bin/time -v cleaner.sh #measures script execution time more precisely than with built-in time
else
    echo "Not timing command."
fi

# check existence of directory
<< 'MULTILINE-COMMENT'
if [ -d "$filepath" ]
then
    echo "Directory $filepath exists."
else
    echo "Error: Directory $filepath does not exists."
    exit 1 # terminate the script
fi

echo "directory: " $filepath # prints the directory name
MULTILINE-COMMENT

# print word counts of the files in folder
echo "Word counts of all txt files in directory"
# for FILE in $filepath; do
for FILE in *.txt; do
    echo "Counting words in " $FILE
    echo "Appending file $FILE to output"
    chkoutput=output #  filename of temporary file
    if test -f "$output"; then # check if specified file exists
        echo "$output exists."
        rm $output  # delete specified file (start with an empty file)
    fi
    cat $FILE >> $chkoutput
done

echo "Counting words..."
# wc -w *.txt | awk '{print $filepath}'; # prints the word count for every file as a number (awk cuts the filename)
wc -w *.txt # prints the word count for every file with the filename

wordconcat=$(wc -w $chkoutput) # words count for concatenated file
echo "Deduplicating output ..."
awk '!X[$0]++' $chkoutput >> $output

echo "Removing temporary file..."
rm $chkoutput # remove temporary file

# echo "Merging and deduplicating files..."
# awk '!a[$0]++' $filepath # merge and deduplicate files in specified folder (https://stackoverflow.com/questions/16873669/combine-multiple-text-files-and-remove-duplicates)

# calculating file sizes
finalbc=$(wc -c < $output) # filesize in bytes
sizeMB=$(bc <<< "scale=2 ; $finalbc / 1024") # filesize in MB
sizeGB=$(bc <<< "scale=2 ; $finalbc / 1024^2") # filesize in GB
echo "Filesize: " $sizeMB "MB, " $sizeGB "GB"

finalwords=$(wc -w $output) #words in final file
echo "Words in final file: " $finalwords
duplicates=$wordconcat-$finalwords
dupepercentage=$(bc <<< "scale=2 ; $duplicates / $wordconcat")
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
