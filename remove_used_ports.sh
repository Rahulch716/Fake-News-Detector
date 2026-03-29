#!/bin/bash

# List of ports you want to clear
PORTS=(8000 5050)

echo "🔍 Checking and clearing ports: ${PORTS[@]}"

for PORT in "${PORTS[@]}"; do
    PID=$(lsof -ti :$PORT)

    if [ -z "$PID" ]; then
        echo "✅ Port $PORT is already free"
    else
        echo "⚠️ Port $PORT is in use by PID(s): $PID"
        echo "🔪 Killing process(es) on port $PORT..."
        kill -9 $PID
        echo "✅ Port $PORT cleared"
    fi
done

echo "🚀 Done!"