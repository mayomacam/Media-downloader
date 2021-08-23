#!/bin/bash
git pull
git add .
read -p "Enter a commit message: " message
git commit -m "$message"
git push -u origin main
