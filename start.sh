

# # 1) setup the dabase folder if doesn't exist 
# db_folder_path="/root/githib_bot_work_space"

# # Check if the folder exists
# if [ ! -d "$db_folder_path" ]; then
#     # If not, create the folder
#     mkdir -p "$db_folder_path"
#     echo ">> Workspace folder created: $db_folder_path"
# else
#     echo ">> Workspace folder already exists: $db_folder_path. Skipping the creation."
# fi



# # If needed use this
# # chmod +x _prod.start.sh

# # TEST:: TO see the config that is being set from env file
# # docker-compose --env-file ./.env.prod -f ./docker-compose.prod.yml config


# # 2) Running the compose for prod 
# docker-compose -f docker-compose.yml up -d --build


pip install -r requirements.txt
python3 main.py