echo "-- Building API --"
docker build -t bidyourauction .

echo "-- Running API --"
docker run -d -p 8080:8080 --name bidyourauction bidyourauction
docker run -it bidyourauction python main.py

