bd_image="postgres"
bd_cointainer="postgres"

api_image="bidyourauction"
api_container="BidYourAuction"

echo "-- Building Database --"
docker build -t $bd_image .
echo "-- Running Database --"
docker run --name $bd_cointainer -p 5432:5432  $bd_image

echo "-- Building API --"
docker build -t bidyourauction .
echo "-- Running API --"
docker run --name $api_container -p 8080:8080 $api_image
