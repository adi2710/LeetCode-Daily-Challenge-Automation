# Daily LeetCoding Challenge Automation

This repository contains automation scripts for Daily LeetCoding Challenge.  
Technology Used : Python

## Content

1. leetcode_POTD.py - To send email reminders and submit Daily LeetCoding Challenge solution if already solved the problem previously.

## Setup

1. Clone/ Download this repo.
2. Setup a python virtual environment and run  
   `pip install -r requirements.txt`
3. Add your `LeetCode's Session` and `csrftoken` in `cred.yml` file. Optional to add `GitHub personal token` there.
4. Also add an `outlook email address` and `password` and your `gmail address` in `cred.yml` to receive email reminders.
4. Run the script and schedule in `AWS Lambda` to run automatically.
