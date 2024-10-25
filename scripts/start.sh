#!/bin/bash

####### /bin/bash start.sh

apply_migrations() {
    echo "Applying migrations..."
    (cd '..' && alembic upgrade head)
    if [ $? -ne 0 ]; then
        echo "Error applying migrations."
    fi
}

downgrade_migrations() {
    echo "Downgrading migrations..."
    (cd '..' && alembic downgrade -1)
    if [ $? -ne 0 ]; then
        echo "Error downgrading migrations."
    fi
}

generate_migrations() {
    if [ -z "$1" ]; then
        echo "No message provided for running the command."
    else
        message="$1"
        if [[ -n "$message" && "$message" =~ [^[:space:]] ]]; then
            echo "Generating migration '$message'..."
            (cd '..' && alembic revision --autogenerate -m "$message")
            if [ $? -ne 0 ]; then
                echo "Error generating migration."
            fi
        else
            echo "Invalid migration message: '$message'."
        fi
    fi
}

apply_initial_data() {
    apply_migrations
    echo "Creating initial data..."
    cd ..
    python app/utils/seeder.py
    if [ $? -ne 0 ]; then
        echo "Error creating initial data."
    fi
}

# Check if any arguments are passed
if [ $# -gt 0 ]; then
    case $1 in
        1)
            apply_migrations
            ;;
        2)
            generate_migrations "$2"
            ;;
        3)
            downgrade_migrations
            ;;
        4)
            apply_initial_data
            ;;
        *)
            echo "Invalid argument. Use 1 for apply, 2 for generate, 3 for downgrade, 4 for initial data."
            ;;
    esac
else
    echo "Select an option:"
    echo "1. Apply migrations"
    echo "2. Generate migrations (with arguments)"
    echo "3. Downgrade migrations"
    echo "4. Create initial data"
    echo "5. Exit"

    read -p "Enter your choice (1-5): " choice

    case $choice in
        1)
            apply_migrations
            ;;
        2)
            read -p "Enter the migration message: " message
            generate_migrations "$message"
            ;;
        3)
            downgrade_migrations
            ;;
        4)
            apply_initial_data
            ;;
        5)
            echo "Exiting."
            exit 0
            ;;
        *)
            echo "Invalid choice. Please select a valid option '(1-5)'."
            ;;
    esac
fi
