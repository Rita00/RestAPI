bd_image="postgres:latest"
bd_cointainer="postgres"

api_image="bidyourauction:latest"
api_container="bidyourauction"

echo "-- Building Database --"
docker build -t $bd_image ./postgres

echo "-- Building API --"
docker build -t $api_container ./api


