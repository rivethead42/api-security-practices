Build the image:
```
docker build -t proxy:latest .
```

Run the container"
```
docker run -d -p 8080:80 proxy:latest
```