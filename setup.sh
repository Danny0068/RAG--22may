#!/bin/bash

# Create .env file
cat > .env << EOL
SUPABASE_URL=${SUPABASE_URL}
SUPABASE_KEY=${SUPABASE_KEY}
GROQ_API_KEY=${GROQ_API_KEY}
EOL

# Install dependencies
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt

# Make run script executable
chmod +x run.sh

# Start the application
./run.sh 