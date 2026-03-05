#!/bin/bash
# Wrapper script for daily Advent Calendar update
# Executed by Launchd

# Navigate to project directory
cd "/Users/norton/Desktop/Cannibisters Agent"

# Log start time
echo "Starting Advent Calendar Update at $(date)"

# Run the python script using the virtual environment python
# Redirect output is handled by launchd but we can also echo here
./.venv/bin/python advent_calendar_manager.py

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Update completed successfully at $(date)"
else
    echo "❌ Update failed with exit code $EXIT_CODE at $(date)"
fi

exit $EXIT_CODE
