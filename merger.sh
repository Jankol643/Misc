#!/bin/bash
<< 'MULTILINE-COMMENT'
    This program merges and deduplicates all files in a folder
    Usage merger.sh
    Date 5/2/2021
    Author Jankol643
    Dependencies: wc (for counting words and file sizes), rm (for removing files), bc (for calculating)
MULTILINE-COMMENT

# Print Header in ASCII Art
# https://www.patorjk.com/software/taag/#p=display&c=echo&f=Doom&t=merger
# Font Doom

echo "                                    ";
echo "                                    ";
echo " _ __ ___   ___ _ __ __ _  ___ _ __ ";
echo "| '_ \` _ \ / _ \ '__/ _\` |/ _ \ '__|";
echo "| | | | | |  __/ | | (_| |  __/ |   ";
echo "|_| |_| |_|\___|_|  \__, |\___|_|   ";
echo "                     __/ |          ";
echo "                    |___/           ";

copyright="(c) 2021 Jankol643"
echo $copyright

echo $separator

separator='---------------------------------------------------------------'
errormsg="Exiting script..."

# check if dependencies are installed
echo "check if dependencies are installed..."
command_exists() {
    # check if command exists and fail otherwise
    command -v "$1" >/dev/null 2>&1
    if [[ $? -ne 0 ]]; then
        echo "I require $1 but it's not installed. Abort."
        echo $errormsg
        exit 1
    fi
}

for COMMAND in "wc" "rm" "bc"; do
    command_exists "${COMMAND}"
done

# filepath=$1 # read file name from command line as argument
# read -p "Enter path: " $filepath # prompt the user to enter a filepath
filepath=./test1/
output="final" #  file name of output file
output=$filepath_$output

# check existence of directory
<< 'MULTILINE-COMMENT'
if [ -d "$filepath" ]
then
    echo "Directory $filepath exists."
else
    echo "Error: Directory $filepath does not exists."
    echo $errormsg
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
    cat $FILE > $chkoutput
done

echo "Counting words..."
# wc -w *.txt | awk '{print $filepath}'; # prints the word count for every file as a number (awk cuts the filename)
wc -w *.txt # prints the word count for every file with the filename

# Calculating file sizes of concatenated file
echo "Calculating file sizes of concatenated file..."
sizeconcat=$(wc -c < $chkoutput) # filesize in bytes of concatenated file
echo $sizeconcat
sizeconcatMB=$(bc <<< "scale=2 ; $sizeconcat / 1024") # filesize in MB
sizeconcatGB=$(bc <<< "scale=2 ; $sizeconcat / 1024^2") # filesize in GB
echo "Filesize:" $sizeconcatMB "MB, " $sizeconcatGB "GB"

wordconcat=$(wc -w < $chkoutput) # words count for concatenated file
echo "No. of words in concatenated file: " $wordconcat

echo "Deduplicating output ..."
awk '!X[$0]++' $chkoutput >> $output

echo "Removing temporary file..."
#rm $chkoutput # remove temporary file

echo $separator

# calculating file sizes
echo "Calculating file sizes of final file..."
finalbc=$(wc -c < $output) # filesize in bytes
sizefinalMB=$(bc <<< "scale=2 ; $finalbc / 1024") # filesize in MB
sizefinalGB=$(bc <<< "scale=2 ; $finalbc / 1024^2") # filesize in GB
echo "Filesize final file:" $sizefinalMB "MB, " $sizefinalGB "GB"

echo "Words in original file: " $wordconcat
finalwords=$(wc -w < $output) #words in final file
echo "Words in final file:" $finalwords
duplicates=$(($wordconcat - $finalwords))
dupepercentage=$(bc <<< "scale=2 ; $duplicates / $wordconcat")
echo "duplicates: " $duplicates ", " "duplicated percentage: " $dupepercentage

# Calcuting saved storage
saved=$(bc <<<"scale=2 ; $sizeconcatMB - $sizefinalMB")
echo "Cleaning saved" $saved "MB of storage."

echo "Script finished successfully. Outputfile: " $output

# Ask user if generated file should be analysed using PACK
while true; do
    read -p "PACK analysis [y/n]" yn
    case $yn in
        [Yy]* ) echo "Yes"; echo "Feeding the file to PACK for analysis"; statsgen $output -o passwords_masks$output; echo $errormsg; exit 0 ;;
        [Nn]* ) echo "No. "; echo $errormsg; exit ;;
        * ) echo "Please answer yes or no." ;;
    esac
done