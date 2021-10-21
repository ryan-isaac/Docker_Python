# Docker_Python
This docker file runs a python code -v 3.8 to download 2 datasets from the web, then process them to generate printed statistics and one excel file with data divided by year for the last 3 years. The URL link for the data could change as it's hosted on Google drive. If you receive an error related to downloading the data and the url, you may need to contact me to update the links inside the '.py' python file.

## Files
- Dockerfile
- requirements.txt
- weather_data.py
- readme.txt
- weather_data.xlsx <= sample output file 
You can build the image from the above or load the image directly from the compressed .tar.gz file
- isaac_docker_python.tar.gz

## Instructions
Please follow below instructions to get the intended output from the program

- 1) Unzip isaac_docker_python.tar.gz
To load this file in a linux environment, make sure you have docker installed and run the following

docker load < isaac_docker_python.tar.gz 

- 2) Run Docker
This python program prints a set of statistics and saves one Excel file named weather_data.xlsx.
This Docker file must be mounted in order to extract the generated file to the host machine. Please mount your desired output directory to the Excel file path inside the container: /usr/src/app/output/ when running the container.

Example:
- To build the container
docker build --tag ryan/python-docker:1 .

- To run the container and save the output file to Downloads directory on your host machine
docker run -it -v ~/Downloads:/usr/src/app/output ryan/python-docker:1



contact email: isaac-ca@outlook.com
