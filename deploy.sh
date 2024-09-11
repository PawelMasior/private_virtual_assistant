# #!/bin/bash

# # Use new location for the files
# # Replace files after new deploy
# # Setup virtualenv & start
# # current deploy folder: ~/actions-runner/_work/virtual_assistant/virtual_assistant#
# # root available
# # chrome installed

# # mkdir "test"


# # =====
# # from chatGPT:
# #!/bin/bash

# # Set variables
# APP_DIR="$HOME"
# APP_DIR2="$GITHUB_WORKSPACE"
# NEW_DIR="new_deploy"
# VENV_DIR="$APP_DIR/venv"
# REQUIREMENTS_FILE="$APP_DIR/requirements.txt"
# MAIN_SCRIPT="$APP_DIR/main.py"

# # Debugging: List contents of new_deploy directory
# echo "Contents of $APP_DIR:"
# if [ -d "$APP_DIR" ]; then
#   ls -la $APP_DIR
# else
#   echo "$APP_DIR does not exist."
#   exit 1
# fi

# echo "Contents of $APP_DIR2:"
# if [ -d "$APP_DIR2" ]; then
#   ls -la $APP_DIR2
# else
#   echo "$APP_DIR2 does not exist."
#   exit 1
# fi

# echo "Contents of $NEW_DIR:"
# if [ -d "$NEW_DIR" ]; then
#   ls -la $NEW_DIR
# else
#   echo "$NEW_DIR does not exist."
#   exit 1
# fi

# # Check if new_deploy directory is not empty
# if [ ! -d "$NEW_DIR" ] || [ -z "$(ls -A $NEW_DIR)" ]; then
#     echo "Directory $NEW_DIR does not exist or is empty."
#     exit 1
# fi

# # Use new location for the files (replacing files with the new deploy)
# echo "Replacing old files with new deployment files..."
# if [ -d "$NEW_DIR" ]; then
#   rm -rf $APP_DIR/*
#   cp -r $NEW_DIR/* $APP_DIR/ || { echo "Failed to copy files from $NEW_DIR to $APP_DIR"; exit 1; }
# else
#   echo "$NEW_DIR does not exist."
#   exit 1
# fi

# # Check if requirements file exists
# if [ ! -f "$REQUIREMENTS_FILE" ]; then
#     echo "Requirements file $REQUIREMENTS_FILE does not exist."
#     exit 1
# fi

# # Setup virtualenv if not already set up
# if [ ! -d "$VENV_DIR" ]; then
#     echo "Creating virtual environment..."
#     python -m venv $VENV_DIR || { echo "Failed to create virtual environment"; exit 1; }
# fi

# # Activate virtualenv
# echo "Activating virtual environment..."
# source $VENV_DIR/bin/activate || { echo "Failed to activate virtual environment"; exit 1; }

# # Install or upgrade dependencies
# echo "Installing dependencies..."
# pip install --no-cache-dir -U pip
# pip install -r $REQUIREMENTS_FILE || { echo "Failed to install dependencies"; exit 1; }

# # Start the Python application
# echo "Starting the Python application..."
# python $MAIN_SCRIPT &

# # Deactivate the virtual environment
# echo "Deactivating virtual environment..."
# deactivate || { echo "Failed to deactivate virtual environment"; exit 1; }

# echo "Deployment completed successfully."
