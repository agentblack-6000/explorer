"""
A NASA API explorer that can get near Earth object data,Mars rover pictures, and
the Astronomy Picture of the Day. Sign up for an API Key at- https://api.nasa.gov,
then set it as an environment variable as follows-

export API_KEY=value

alternatively use DEMO_KEY if you don't want to sign up-

export API_KEY="DEMO_KEY"

Run the explorer with the following command line arguments-

options:
  -h, --help            show this help message and exit
  -as start_date end_date, --asteroids start_date end_date
                        write near Earth object data to a csv file and print 'rows' rows of data
  -ap date file_name, --apod date file_name
                        save the Astronomy Picture of the Day('date') as 'file_name'(no extension)
  -m file_name date, --mars file_name date
                        write the Mars rover image urls to a text file
"""
import csv
import datetime as dt
import os
import re
import sys
from argparse import ArgumentParser

import requests

API_KEY = os.environ.get("API_KEY")
DATE = re.compile(r"(\d\d\d\d)-(\d\d)-(\d\d)")
TIMEOUT = 20


def main():
    """
    Validates the API key and command line arguments using argparse, then calls
    the relevant methods.

    :returns: None
    """

    # Validate API key
    if not API_KEY:
        sys.exit("API Key not set")

    # Create argument parser and add optional command line arguments
    parser = ArgumentParser(description="A NASA API explorer that can get near Earth object data, "
                                        "Mars rover pictures, and the Astronomy "
                                        "Picture of the Day.")
    parser.add_argument("-as", "--asteroids", nargs=2, metavar=("start_date", "end_date"),
                        dest="asteroid", help="write near Earth object data to a csv "
                             "file and print 'rows' rows of data")
    parser.add_argument("-ap", "--apod", nargs=2, dest="apod", metavar=("date", "file_name"),
                        help="save the Astronomy Picture of the Day('date') "
                             "as 'file_name'(no extension)")
    parser.add_argument("-m", "--mars", nargs=2, dest="mars", metavar=("file_name", "date"),
                        help="write the Mars rover image urls to a text file")

    # Parse arguments
    args = parser.parse_args()

    # Validate at least flag was given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    # Call the relevant methods with provided command line arguments
    if args.asteroid is not None:
        start, end = args.asteroid
        explore_asteroids(start, end)
    elif args.apod is not None:
        date, file_name = args.apod
        explore_apod(date, file_name)
    elif args.mars is not None:
        file_name, date = args.mars
        explore_mars_rover_photos(file_name, date)


def explore_asteroids(start_date: str, end_date: str) -> int:
    """
    Writes NASA's Asteroids - NeoWs (Near Earth Object Web Service) data to a CSV file, based on
    the given start and end date. See NASA's Asteroids - NeoWs API at https://api.nasa.gov for more
    information and to sign up for an API key.

    Data set provided by- https://cneos.jpl.nasa.gov (CNEOS is NASA's center for computing
    asteroid and comet orbits and their odds of Earth impact).

    :param start_date: The start date
    :type start_date: str
    :param end_date: The end date
    :type end_date: str
    :returns: The response code after making request
    :rtype: int
    """

    # Using regexes, validates start and end date
    if not re.search(DATE, start_date):
        print("Invalid date, use YYYY-MM-DD.")
        return False
    if not re.search(DATE, end_date):
        print("Invalid date, use YYYY-MM-DD.")
        return False

    # Checks to see if end date is after start date
    start_year, start_month, start_day = start_date.split("-")
    end_year, end_month, end_day = end_date.split("-")
    try:
        start = dt.datetime(year=int(start_year), month=int(start_month), day=int(start_day))
        end = dt.datetime(year=int(end_year), month=int(end_month), day=int(end_day))
    except ValueError:
        print("Invalid dates, use correct values for year, month, day.")
        return False

    if start > end:
        print("Invalid dates, end date must be after start date.")
        return False

    # Sets up request parameters
    asteroids_endpoint = "https://api.nasa.gov/neo/rest/v1/feed?"
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "api_key": API_KEY,
    }

    print("Getting API response...")
    # Gets the API response
    api_response = requests.get(asteroids_endpoint, params, timeout=TIMEOUT)
    asteroid_response = api_response.json()

    try:
        log = asteroid_response["near_earth_objects"]
    except KeyError:
        print("Invalid date/API key. Check if API key is valid and end date is within "
              "7 days of the start date")
        return False

    print("Writing data to csv file...")
    file_name = "near_earth_object_data.csv"
    # Opens a new csv file and writes data
    with open(file_name, "w", encoding="utf-8") as file:

        # Writes data to csv using DictWriter
        field_names = ["date", "name", "estimated_diameter_min_meters",
                       "estimated_diameter_max_meters", "estimated_diameter_min_feet",
                       "estimated_diameter_max_feet"]
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()

        for date in log:
            for near_earth_object in log[date]:
                name = near_earth_object["name"]

                estimated_diameter_meters = near_earth_object["estimated_diameter"]["meters"]
                estimated_diameter_min_meters = round(
                    estimated_diameter_meters["estimated_diameter_min"], 2)
                estimated_diameter_max_meters = round(
                    estimated_diameter_meters["estimated_diameter_max"], 2)

                estimated_diameter_feet = near_earth_object["estimated_diameter"]["feet"]
                estimated_diameter_min_feet = round(
                    estimated_diameter_feet["estimated_diameter_min"], 2)
                estimated_diameter_max_feet = round(
                    estimated_diameter_feet["estimated_diameter_max"], 2)

                near_earth_object_data = {
                    "date": date,
                    "name": name,
                    "estimated_diameter_min_meters": estimated_diameter_min_meters,
                    "estimated_diameter_max_meters": estimated_diameter_max_meters,
                    "estimated_diameter_min_feet": estimated_diameter_min_feet,
                    "estimated_diameter_max_feet": estimated_diameter_max_feet
                }
                writer.writerow(near_earth_object_data)

    print(f"Finished writing data to {file_name}.")
    return api_response.status_code


def explore_apod(date: str, file_name: str) -> int:
    """
    Saves the Astronomy Picture of the Day from NASA's APOD API with the specified file name.
    See NASA's APOD API at https://api.nasa.gov for more information and to signup for an
    API key.

    See API documentation at https://github.com/nasa/apod-api, and the APOD website
    at- https://apod.nasa.gov/apod/astropix.html

    :param file_name: The file name of the image that will be saved
    :type file_name: str
    :param date: The date to get the Astronomy Picture of the Day from
    :type date: str
    :return: API response code
    :rtype: int
    """

    # Validates date using regex
    if not re.search(DATE, date):
        print("Invalid date format, use YYYY-MM-DD.")
        return False

    # Checks if file name exists
    if not file_name or file_name == " ":
        print("Invalid file name.")
        return False

    # Sets up request parameters
    apod_endpoint = "https://api.nasa.gov/planetary/apod"
    params = {
        "date": date,
        "api_key": API_KEY
    }

    print("Getting API response...")
    # Gets API response
    apod_response = requests.get(apod_endpoint, params, timeout=TIMEOUT)
    apod_response_json = apod_response.json()
    try:
        image_url = apod_response_json["hdurl"]
    except KeyError:
        print("Invalid date/API key. Check if API key is valid and date is not after today.")
        return False

    # Gets image file extension from url
    file_extension = os.path.splitext(image_url)[-1]
    file_name = f"{file_name}{file_extension}"

    print("Saving image...")
    # Gets the image and saves it
    image = requests.get(image_url, timeout=TIMEOUT)

    with open(file_name, 'wb', encoding=None) as file:
        file.write(image.content)

    print(f"Saved image as {file_name}.")

    return apod_response.status_code


def explore_mars_rover_photos(file_name: str, date: str):
    """
    Accesses NASA's Mars Rover Photos API, and puts image urls taken by the Curiosity Mars rover
    in specified text file, and saves the first image found. See NASA's Mars Rover Photos API at
    https://api.nasa.gov for more information and to signup for an API key.

    See the API documentation at https://github.com/corincerami/mars-photo-api

    :param date: The date to photos were captured, can't be today
    :type date: str
    :param file_name: The text file to write the image URLs
    :type file_name: str
    :returns: API response code
    :rtype: int
    """
    # Using regex, validates date
    if not re.search(DATE, date):
        print("Invalid date format, use YYYY-MM-DD.")
        return False

    # Check if file name is valid
    if not file_name or file_name == " " or not file_name.endswith("txt"):
        print("Invalid file name, must contain characters and end with .txt .")
        return False

    date_year, date_month, date_day = date.split("-")
    try:
        date_dt = dt.datetime(year=int(date_year), month=int(date_month), day=int(date_day))
    except ValueError:
        print("Invalid date, use correct values for year, month, day")
        return False

    if date_dt > dt.datetime.today():
        print("Date must not be after today.")
        return False

    # Sets up request parameters
    mars_endpoint = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"
    params = {
        "earth_date": date,
        "api_key": API_KEY
    }

    print("Getting API response...")
    # Gets API response
    api_response = requests.get(mars_endpoint, params, timeout=10)
    rover_images = api_response.json()

    try:
        photos = rover_images["photos"]
    except KeyError:
        print("Invalid date/API key.")
        return False

    images = []
    print(f"Saving urls to {file_name}...")
    # Writes url to file
    with open(file_name, "w", encoding="utf-8") as file:
        for photo in photos:
            image_url = photo['img_src']
            file.write(f"{image_url}\n")

            images.append(image_url)

    print(f"Saved urls to {file_name}.")

    # Gets image if images were found
    try:
        file_extension = os.path.splitext(images[0])[-1].lower()
    except IndexError:
        sys.exit()

    print("Saving first image...")
    # Gets image and saves it
    file_name = f"mars{file_extension}"
    image = requests.get(image_url, timeout=10)

    with open(file_name, 'wb', encoding=None) as file:
        file.write(image.content)

    print(f"Image saved as {file_name}.")
    return api_response.status_code


if __name__ == "__main__":
    main()
