#!/bin/bash
<<'MULTILINE-COMMENT'
This program reads a filename from STDIN and cleans the file
Script must be in same folder as specified file
Usage ./cleaner.sh filename.txt
Date 5/2/2021
Author Jankol643
Dependencies: bc for calculation, time for measuring execution time, awk, wc
MULTILINE-COMMENT

separator='---------------------------------------------------------------'
errormsg="Exiting script..."
tempoutput="temp"
defaultoutputdir="cleaned" # path to output directory

# Print Header in ASCII Art
# https://www.patorjk.com/software/taag/#p=display&c=echo&f=Doom&t=cleaner
# Font Doom

print_header(){
  echo "      _                            ";
  echo "     | |                           ";
  echo "  ___| | ___  __ _ _ __   ___ _ __ ";
  echo " / __| |/ _ \/ _\` | '_ \ / _ \ '__|";
  echo "| (__| |  __/ (_| | | | |  __/ |   ";
  echo " \___|_|\___|\__,_|_| |_|\___|_|   ";
  echo "                                   ";
  echo "                                   ";
}

print_header

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

checkFile(){
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
  echo $2
  exit 1 # terminate the script
fi
else
  echo "$1 is not a text file. Please specify a text file (.txt)."
  echo "Usage: ./cleaner.sh filename.txt"
  echo $2
  exit 1 # terminate the script
fi
else # file is not found
  echo "$1 doesn't exist."
  echo "Usage: cleaner.sh filename.txt"
  echo $2
  exit 1 # terminate the script
fi
}

print_info(){
  # print general information about the file
  echo "print general information about the file"
  echo "filename" $1           # prints the filename
  nolines=$(wc -l <$1)         # saves the no. of lines in a variable
  echo "no. of lines" $nolines # prints the number of lines
  nowords=$(wc -w <$1)         # saves the no. of words in a variable
  echo "number of words" $nowords # prints the number of words
}

# Sorting file
sorting(){
  # check if file is sorted
  if sort -C $1; then
    # return code 0
    echo "sorted"
  else
    # return code not 0
    echo "not sorted"
    startsort=`date +%s.%N`
    echo "sort file alphabetically"
    sort -o ${1}_occur.txt # sort by no. of occurences
    endsort=`date +%s.%N`
    runtimesort=$( echo "$endsort - $startsort" | bc -l )
    echo "Runtime sorting (by no. of occurences): " $runtimesort
  fi
}

# Deduplicating file
deduplicating(){
  startdedup=`date +%s.%N`
  echo "remove duplicates"
  awk '!visited[$0]++' ${1}_occur.txt > $tempoutput # remove duplicates, https://iridakos.com/programming/2019/05/16/remove-duplicate-lines-preserving-order-linux
  enddedup=`date +%s.%N`
  runtimededup=$( echo "$enddedup - $startdedup" | bc -l )
  echo "Runtime deduplication: " $runtimededup
}

wordcount(){
  echo "Counting words and duplicates..."
  finalwords=$(wc -w < $tempoutput) #words in final file
  echo "Words in final file: " $finalwords
  duplicates=$(($nowords - $finalwords))
  dupepercentage=$(bc <<<"scale=2 ; $duplicates / $nowords")
  echo "duplicates: " $duplicates ", " "duplicated percentage: " $dupepercentage
}

filesizes(){
  # calculating file sizes
  echo "Calculating file sizes..."
  echo "Original file: "
  fileb=$(wc -c < $filename) # filesize in bytes
  filemb=$(bc <<<"scale=2 ; $fileb / 1024") # filesize in MB
  echo "Filesize MB: " $filemb
  filegb=$(bc <<<"scale=2 ; $fileb / 1024^2") # filesize in GB
  echo "Filesize GB: " $filegb
}

readfilepath(){
  # Read user specified output file path
  while true; do
    read -p "Please enter output file path: " useroutputdir
    #useroutputdir = ${useroutputdir:-$defaultoutputdir} # parameter expansion
    # take the value the user enters, if none is specified, fall back to specified default value
    if [ $useroutputdir=="" ]; then
      echo "Path is empty."
      echo "Falling back to default value" $defaultoutputdir
      $useroutputdir=$defaultoutputdir
    else
      echo "Reading user input for file path ..."
      $useroutputdir=$1
    fi

    # check if output directory exists
    if [ -d "$useroutputdir" ]; then
      echo "$useroutputdir is a directory."
      break
      # elif [ $useroutputdir -lt 1 ] #  file arguments less than 1 => no arguments given
      # then
      #     echo "Incorrect Usage"
      #     echo $errormsg
      #     exit 1
    elif [ ! -d "$useroutputdir" ] # directory does not exist
    then
      echo "Directory does not exist, creating it ..."
      mkdir $useroutputdir # create folder
      break
    else
      echo "Some other problem"
      echo $errormsg
      exit 1
    fi

  done
}

# Ask the user for the output file name
readoutputfile(){
  while true; do
    read -p "Please enter output file: " outputfile
    if [ $outputfile=='' ];  then
      echo "Output file string empty."
      defaultoutput=$filename # set default to entry filename
      output=$defaultoutput
      echo "Falling back to default" $defaultoutput
      break
    else
      echo "Taking user input..."
      output=$outputfile #  file name of output file
      break
    fi
  done
}

fileanalysis(){
  # Ask user if generated file should be analysed using PACK
  while true; do
    read -p "PACK analysis [y/n]" yn
    case $yn in
      [Yy]* ) echo "Yes"; echo "Feeding the file to PACK for analysis"; statsgen $output -o passwords_masks$output; echo $errormsg; exit 0 ;;
      [Nn]* ) echo "No. "; echo $errormsg; exit ;;
      * ) echo "Please answer yes or no." ;;
    esac
  done
}

for COMMAND in "bc" "awk" "wc"; do
  command_exists "${COMMAND}"
done

filename=$1    # read file name from command line as argument

checkFile $filename $errormsg
echo $separator
print_info $filename
echo $separator

sorting $filename
deduplicating

echo "Deleting temporary file..."
rm ${1}_occur.txt # delete temporary file

echo $separator
wordcount $tempoutput
echo $separator
filesizes $filename
echo $separator
filesizes $tempoutput
echo $separator

# Calcuting saved storage
saved=$(bc <<<"scale=2 ; $filemborig - $filembclean")
echo "Cleaning saved " $saved "MB of storage."

echo "Script finished successfully. Outputfile: " $tempoutput

readfilepath
readoutputfile

# Moving the output file to specified folder
echo "Moving the output file to specified folder..."
mv $tempoutput $useroutputdir/$output
#mv $output $defaultoutputdir/$output

echo $separator

packanalysis
