# Explorer
#### Description:
A NASA API explorer that can get near Earth object data, Mars rover pictures, and
the Astronomy Picture of the Day. 

## Usage
Sign up for an API Key at- https://api.nasa.gov, then set it as an environment variable as follows-
```
$ export API_KEY=value
```
alternatively, if you don't wish to sign up, export the API key as follows-
```
$ export API_KEY=DEMO_KEY
```
Run the explorer with the following command line arguments-
- ```-h```: Display the help page
- ```-as start_date end_date```: Explore NASA's Asteroids - NeoWs (Near Earth Object Web Service).
- ```-ap date file_name```: Explore the Astronomy Picture of the Day from NASA's APOD API.
- ```-m file_name date```: Explore NASA's Mars Rover Photos API.
```
$ python project.py [-h] [-as start_date end_date] [-ap date file_name] [-m file_name date]
```

## Project Overview
Explorer is a NASA API explorer that gets data from NASA's open APIs: Asteroids - NeoWs, APOD, and Mars Rover Photos
![APOD for 2022-12-30](image.jpg)
The Astronomy Picture of the Day for December 30, 2022, accessed by-
```
$ python project.py -ap 2022-12-30 image
```

## Project Files
### ```project.py```
The implementation of Explorer, that has the following functions-
##### ```main()```:  
Validates the API key and command line arguments using Python's argparse and sys, and then calls the relevant functions 
below.

##### ```explore_asteroids(start_date: str, end_date: str) -> int```:
Writes NASA's Asteroids - NeoWs (Near Earth Object Web Service) data to a CSV file, based on
the given start and end date.

1. First using a regex(using Python's ```re``` module), it checks if the dates provided in the correct format, 
   and then uses ```datetime``` to verify dates are valid.
2. Then, uses ```requests``` with NASA's Asteroids - NeoWs (Near Earth Object Web Service) API 
   endpoint (https://api.nasa.gov/neo/rest/v1/feed?) with the provided dates and API key. 
3. Then converts the response data to JSON and writes the data to a csv file using ```DictWriter```, and returns the
   response status code.

##### ```explore_apod(date: str, file_name: str) -> int```:
Saves the Astronomy Picture of the Day from NASA's APOD API with the specified file name.

1. First using a regex(using Python's ```re``` module), it checks if the dates provided in the correct format, 
   then validates the file name.
2. Then, uses ```requests``` with the APOD API endpoint (https://api.nasa.gov/planetary/apod) 
   with the provided date and API key. 
3. Then converts the response data to JSON, gets the image url, and then using ```requests```, gets the image
   and writes it to the specified file.

##### ```explore_mars_rover_photos(file_name: str, date: str) -> int```:
Accesses NASA's Mars Rover Photos API, and puts image urls taken by the Curiosity Mars rover in specified text file, 
and saves the first image found.
1. First using a regex(using Python's ```re``` module), it checks if the dates provided in the correct format, 
   validates the file name, and uses ```datetime``` to check if the date is valid.
2. Then, uses ```requests``` with the Mars Rover Photos API endpoint 
   (https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos) with the provided date and API key. 
3. Then converts the response data to JSON, gets the image urls, and writes them to a text file.
4. Saves the first image found.

### ```test_project.py```
Unit tests for the functions implemented in project.py-
##### ```test_explore_asteroids()```
- Tests invalid dates.
- Verifies status codes.
##### ```test_explore_apod()```
- Tests invalid dates and file names.
- Verifies status codes.
##### ```test_explore_mars_rover_photos()```
- Tests invalid dates, file names, and file extensions.
- Verifies status codes.

### ```requirements.txt```
The ```pip```-installable libraries required.
- ```requests```

### How do I get started?
1. Clone the repository
2. Run the Explorer as follows-
```
$ python project.py [-h] [-as start_date end_date] [-ap date file_name] [-m file_name date]
```

### How do I clone the repository?
To clone the repository, execute-
```
$ git clone https://github.com/agentblack-6000/explorer.git
```