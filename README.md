                                                              # Data_streaming

This side project was made with "learning the data engineering process" in mind.
so i made a program that stream data from twitter, following some rules that user can set in "data_sources.json" file.
and the same time store all the incoming data into a mysql data.

# Further update :
- apply sentiment Analysis on the stored data
- update my database from another source of data.

# technologies
- python.
- docker (mysql, phpmyadmin).

# usage : - before executing the "figure_it_out.py" you have to execute "./get_bearer.sh <api_key> <api_secret_key>".
            it will generate a "bearer token" and store it along with your <api-key> <api_secret_key> in env variables named :
            * ACCESS_TOKEN_TWT
            * API_KEY_TWT
            * API_SECRET_TWT
          - you can activate and de-activate log output on screen, by changin the "data_sources/log" value in the  "data_sources.json" file. 
