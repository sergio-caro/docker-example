FROM postgres:latest
COPY create_fixtures.sql /docker-entrypoint-initdb.d/create_fixtures.sql


# Create the docker image 
# docker build -t <image_id:version> . 
# Run the docker image and connect to it
# docker run --rm -P --publish 127.0.0.1:5432:5432 --name <container_name> <image_id>
# Enter to the database
# psql postgres://username:secret@localhost:5432/database