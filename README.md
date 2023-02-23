# Project TestFeedbacksWithChatGPT

TestFeedbacksWithChatGPT - Allows you to rank your data using ChatGPT

## Installation

1. Clone the repository
2. Create a virtual environment
3. Install dependencies 'pip install -r requirements.txt'
4. Create .env, write your 'API_KEY="your_key"'

## Requirements for the format of data

1. Data in .csv
2. Identifier - the first column (in my case - email)
3. Data in second column

## Request to ChatGPT
Describe the required work with the data in 'request_to_chatgpt'

## Result

1. in "filename"_analyzed.csv
2. The columns correspond to the original data structure. And will be added a third with the result of processing