#!/bin/bash

# Configuration
SERVER="localhost:8080"
NODE="test"
TOKEN="token1234"
CONNECTION_IPS=("127.0.0.1" "1.1.1.1" "8.8.8.8")

# Get the current timestamp
stamp=$(date +%s)

# Initialize an associative array to store connection timestamps
declare -A connection_timestamps

# Check connections and store timestamps
for ip in "${CONNECTION_IPS[@]}"; do
    if ping -c 1 $ip | grep -q "from"; then
        connection_timestamps[$ip]=$stamp
    else
        connection_timestamps[$ip]="null"
    fi
done

# Build JSON payload dynamically
json_data="{"
json_data+="\"server\": \"$NODE\", \"token\": \"$TOKEN\""

for ip in "${!connection_timestamps[@]}"; do
    json_data+=", \"$ip\": ${connection_timestamps[$ip]}"
done

json_data+="}"

# Send HTTP POST request with JSON data
curl -k -X POST -H "Content-Type: application/json" -d "$json_data" "http://$SERVER/ping"
echo $json_data
