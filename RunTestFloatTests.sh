#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <folder_path> <rounding>"
    exit 1
fi

folder_path="$1"
rounding="$2"

# Check if folder exists
if [ ! -d "$folder_path" ]; then
    echo "Unknown folder: $folder_path"
    exit 1
fi

# Loop through all files in the folder
for file in "$folder_path"/*; do
    if [ -f "$file" ]; then
        # Get the operation from the file name
        filename=$(basename "$file")
        format="${filename%%_*}"
        operation="${filename%.*}"  # Extract operation from filename (remove extension)
        operation="${operation##*_}"  # Extract operation after last underscore
        # Run the test script on each file with its respective operation
        echo -e "Executing $file..."
        time python runner_test_float.py "$format" "$file" "$operation" "$rounding"
    fi
done
