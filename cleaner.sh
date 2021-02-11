#!/bin/bash
<<'MULTILINE-COMMENT'
    This program reads a filename from STDIN and cleans the file
    Script must be in same folder as specified file
    Usage ./cleaner.sh filename.txt
    Date 5/2/2021
    Author Jankol643
    Dependencies: bc for calculation, time for measuring execution time, awk, wc
    TODO: Calculation saved storage
MULTILINE-COMMENT

separator='---------------------------------------------------------------'
echomsg="Exiting script..."

output="final" #  file name of output file

# Print Header in ASCII Art
# https://www.patorjk.com/software/taag/#p=display&c=echo&f=Doom&t=cleaner
# Font Doom

echo "      _                            ";
echo "     | |                           ";
echo "  ___| | ___  __ _ _ __   ___ _ __ ";
echo " / __| |/ _ \/ _\` | '_ \ / _ \ '__|";
echo "| (__| |  __/ (_| | | | |  __/ |   ";
echo " \___|_|\___|\__,_|_| |_|\___|_|   ";
echo "                                   ";
echo "                                   ";

copyright="(c) 2021 Jankol643"
echo $copyright

echo $separator

# check if dependencies are installed
echo "check if dependencies are installed..."
command_exists() {
    # check if command exists and fail otherwise
    command -v "$1" >/dev/null 2>&1
    if [[ $? -ne 0 ]]; then
        echo "I require $1 but it's not installed. Abort."
        exit 1
    fi
}

for COMMAND in "bc" "awk" "wc"; do
    command_exists "${COMMAND}"
done

filename=$1    # read file name from command line as argument

# Check if user specified file exists, is a text file and has data
echo "Check if file exists..."
if [ -f "$1" ]; then # file exists
    echo "$1 exists."
    echo "Checking if file is a text file ..."
    if [[ "$1" == *.txt ]]; then # file is a txt file
        echo "Check if file is empty..."
        if [ -s "$1" ]; then     # file has data
            echo "$1 has some data."
            # do something as file has data
        else
            echo "$1 is empty."
            echo "Exiting..."
            exit 1 # terminate the script
        fi
    else
        echo "$1 is not a text file. Please specify a text file (.txt)."
        echo "Usage: ./cleaner.sh filename.txt"
        echo "Exiting..."
        exit 1 # terminate the script
    fi
else # file is not found
    echo "$1 doesn't exist."
    echo "Usage: cleaner.sh filename.txt"
    echo "Exiting..."
    exit 1 # terminate the script
fi

echo $separator

# print general information about the file
echo "print general information about the file"
echo "filename" $1           # prints the filename
nolines=$(wc -l <$1)         # saves the no. of lines in a variable
echo "no. of lines" $nolines # prints the number of lines
nowords=$(wc -w <$1)         # saves the no. of words in a variable
echo "number of words" $nowords # prints the number of words

echo $separator

# Sorting and deduplicating
echo "sort by no. of occurences"
sort -n $1 >${1}_occur.txt # sort by no. of occurences
echo "remove duplicates"
awk '!visited[$0]++' ${1}_occur.txt >$output # remove duplicates, https://iridakos.com/programming/2019/05/16/remove-duplicate-lines-preserving-order-linux

echo "Deleting temporary file..."
rm ${1}_occur.txt # delete temporary file

echo $separator

# Counting words and duplicates
echo "Counting words and duplicates..."
finalwords=$(wc -w <$output) #words in final file
echo "Words in final file: " $finalwords
duplicates=$(($nowords - $finalwords))
dupepercentage=$(bc <<<"scale=2 ; $duplicates / $nowords")
echo "duplicates: " $duplicates ", " "duplicated percentage: " $dupepercentage

echo $separator

# calculating file sizes
echo "Calculating file sizes..."
echo "Original file: "
fileborig=$(wc -c <$1) # filesize in bytes
filemborig=$(bc <<<"scale=2 ; $fileborig / 1024") # filesize in MB
echo "Filesize MB: " $filemborig
filegborig=$(bc <<<"scale=2 ; $fileborig / 1024^2") # filesize in GB
echo "Filesize GB: " $filegborig

echo $separator

# calculating file sizes
echo "Calculating file sizes..."
echo "Cleaned file: "
filebclean=$(wc -c <$output) # filesize in bytes
filembclean=$(bc <<<"scale=2 ; $filebclean / 1024") # filesize in MB
echo "Filesize MB: " $filembclean
filegbclean=$(bc <<<"scale=2 ; $filebclean / 1024^2") # filesize in GB
echo "Filesize GB: " $filegbclean

echo $separator

# Calcuting saved storage
saved=$(bc <<<"scale=2 ; $filemborig - $filembclean")
echo "Cleaning saved " $saved "MB of storage."

echo "Script finished successfully. Outputfile: " $output

echo $separator

# Ask user if generated file should be analysed using PACK
while true; do
    read -p "PACK analysis [y/n]" yn
    case $yn in
        [Yy]* ) echo "Yes"; echo "Feeding the file to PACK for analysis"; statsgen $output -o passwords_masks$output; echo $echomsg; exit 0 ;;
        [Nn]* ) echo "No. "; echo $echomsg; exit ;;
        * ) echo "Please answer yes or no." ;;
    esac
done