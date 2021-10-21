# Docker_Python
This docker file runs a python code -v 3.8 to download 2 datasets from the web, then process them to generate printed statistics and one excel file with data divided by year for the last 3 years. The URL link for the data could change as it's hosted on Google drive. If you receive an error related to downloading the data and the url, you may need to contact me to update the links inside the '.py' python file.

## Files
- Dockerfile
- requirements.txt
- weather_data.py
- readme.txt
- weather_data.xlsx <= sample output file
 
## Instructions
This python program prints a set of statistics and saves one Excel file named weather_data.xlsx.
This Docker file must be mounted in order to copy the saved file to the host machine. Please mount your desired output directory to the Excel file path inside the container: /usr/src/app/output/ when running the container.

Please follow below example code to get the intended output from the program.

Example:
- To build the container
Save the files (Dockerfile, requirements.txt, weather_data.py) in one directory and run the following inside the same directory

$ docker build --tag ryan/python-docker:1 .

- To run the container and save the output file to Downloads directory on your host machine

$ docker run -it -v ~/Downloads:/usr/src/app/output ryan/python-docker:1

- Compress and save the container image:
You can save the built image and run it somewhere else directly from a compressed .tar.gz file. The compressed image will be around 100MB as it holds all the packages and modules required to run the program.

$ docker save ryan/python-docker:1 | gzip > isaac_docker_python.tar.gz

- Unzip and load isaac_docker_python.tar.gz
To load this file in a linux environment, make sure you have docker installed and run the following

$ docker load < isaac_docker_python.tar.gz 





contact email: isaac-ca@outlook.com
