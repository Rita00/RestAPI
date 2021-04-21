bd_image="postgres:latest"
bd_cointainer="postgres"

echo "-- Running Database --"
docker stop $bd_cointainer || true && docker rm $bd_cointainer || true
docker run --name $bd_cointainer -p 5432:5432  $bd_image

