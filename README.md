Everything needed for the server application.

This is an updated version that runs on either Apache or Flask.

## Usage

Clone this repository onto your machine.

`cd` into the repository and run `docker-compose up`.

Alternatively, just run `bash launch.sh`.

The server will start on port 2000. To access, go to `http://localhost:2000`.

**Important**

If you are running on a Raspberry Pi, you must uncomment the following line in [db/Dockerfile](db/Dockerfile):
```
RUN dpkg --add-architecture armhf
```

## Updates

`cd` into the repository and run the following commands.
```
git pull
docker-compose down && docker-compose up
```

## Logs

You may access the application logs with the following command.
```
docker logs server_app_1 -f
```

## Notes

You may run `docker-compose up -d` to run as a background service.