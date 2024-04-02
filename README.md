Using python 3.11
The code uses chromium instead of the specified chrome because this is what I have installed on my computer

To run locally outside docker one should also run `playwright install` after installing dependencies

To create or update the har test file change update=True and run the test


build the docker normally:
docker build -t browser_module -f browser_module.Dockerfile .

run with the example:
docker run -v ./dockertest:/input -v ./dockertest:/output -it browser_module