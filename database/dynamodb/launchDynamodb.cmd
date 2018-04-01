echo "webinterface: http://localhost:8000/shell/"

java -Djava.library.path=./dynamodb_local_latest/DynamoDBLocal_lib -jar ./dynamodb_local_latest/DynamoDBLocal.jar  -dbPath ./db_store -sharedDb