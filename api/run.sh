api_image="bidyourauction:latest"
api_container="bidyourauction"

echo "-- Running API --"
docker stop $api_container || true && docker rm $api_container || true
docker run --name $api_container -p 8080:8080 $api_image

