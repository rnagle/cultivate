#!/bin/bash

if [ ! -f "get_access_token.py" ]; then
  wget -O get_access_token.py \
    "https://raw.githubusercontent.com/bear/python-twitter/master/get_access_token.py" &> /dev/null;
fi

python get_access_token.py;

echo "
Create a file named '.env' in the project directory and save your access
token key and access token secret in said file in the following format:

export TWITTER_ACCESS_TOKEN_KEY=\"TOKENKEYGOESHERE\"
export TWITTER_ACCESS_TOKEN_SECRET=\"TOKENSECRETGOESHERE\"
";
