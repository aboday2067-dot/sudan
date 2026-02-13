#!/bin/bash
cd /home/user/webapp

# Kill any existing Python processes
pkill -9 python 2>/dev/null || true
sleep 2

# Unset old environment variables
unset OPENAI_API_KEY
unset GROQ_API_KEY
unset AI_MODEL

# Start the app
python app.py
