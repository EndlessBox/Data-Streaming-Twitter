#!/usr/bin/env bash

grant="grant_type=client_credentials"
api_url="https://api.twitter.com/oauth2/token"
env_var="ACCESS_TOKEN_TWT"
api_key="API_KEY_TWT"
api_secret="API_SECRET_TWT"

if [[ -z $0 ]] || [[ -z $1 ]]; then
	echo "Usage : source ./get_bearer.sh <API_KEY> <API_SECRET_KEY>"
	echo " OR"
	echo "Usage : . ./get_bearer.sh <API_KEY> <API_SECRET_KEY>"
else
	bearer_token=$(curl -u $1:$2 --data ${grant} ${api_url})
	clear_bearer_token=$(echo ${bearer_token} | cut -d '"' -f8)
	export ${env_var}=${clear_bearer_token}
	export ${api_key}=$1
	export ${api_secret}=$2
	echo "Bearer Token saved succefuly on : ${env_var}"
	echo "API Key saved succefuly on : ${api_key}"
	echo "API Secret saved succefuly on : ${api_secret}"
	echo "Use : 'echo \$${env_var}'"
	echo "Use : 'echo \$${api_key}'"
	echo "Use : 'echo \$${api_secret}'"
fi
