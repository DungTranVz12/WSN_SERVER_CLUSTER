#!/bin/bash

# Sleep for 10 seconds
sleepNum=15
i=0

# Print out the sleep time every 1 second
while [ "$i" -lt "$sleepNum" ]; do
  echo "Sleep: $i/$sleepNum"
  sleep 1
  i=$((i+1))
done




# input_string="Hello @World! \/?123"


# # Loại bỏ các ký tự đặc biệt và thay thế khoảng trắng bằng gạch dưới
# cleaned_string=$(echo "$input_string" | sed -e 's/[^A-Za-z0-9]/_/g')

# # In chuỗi đã được xử lý
# echo "$cleaned_string"

# fileName="/file.txt"

# echo "cleaned_string" | tee "$fileName"


