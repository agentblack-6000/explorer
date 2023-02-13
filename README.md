| name        | description                                           | author          | img                                                        |
|-------------|-------------------------------------------------------|-----------------|------------------------------------------------------------|
| PyCuriosity | API explorer that gets Curiosity's(Mars rover) images | @agentblack6000 | https://cloud-8qn1gonwl-hack-club-bot.vercel.app/0mars.jpg |

# PyCuriosity
Build an API explorer that gets images from Curiosity, a NASA Mars rover, such as this one!
![One of Curiosity's images](https://cloud-8qn1gonwl-hack-club-bot.vercel.app/0mars.jpg)

This workshop should take about ~30 min.

## Project Overview
PyCuriosity is an API explorer that gets Curiosity's images and image urls. 

If you haven't worked with APIs before, read this [resource](https://www.ibm.com/in-en/topics/api). In short, 
**A**pplication **P**rogramming **I**nterfaces(APIs for short) enable different computer applications to communicate, 
which is useful because we want images from Curiosity, which are stored on NASA's servers. To access them, we need a way 
to communicate with NASA's servers, which may seem daunting, but all we need to do is make a [GET request](https://rapidapi.com/blog/api-glossary/get)
to one of NASA's APIs, or request information from NASA's servers.

You can browse through NASA's APIs at [api.nasa.gov](https://api.nasa.gov/), and sign up for an API key if you want.
This isn't strictly required, as we'll see later on. The API we'll be using in this workshop is called the [Mars Rover Photos API](https://github.com/corincerami/mars-photo-api),
an API for, well, Mars rover photos.

For simplicity, we won't create a GUI, but rather enable program execution using command line arguments(arguments that
can modify the flow of a program), using Python's builtin ```argparse```, a powerful library to parse command line arguments.

After validating the command line arguments, we'll call the Mars Rover Photos API, using ```requests```, and then write
the data to a text file, and potentially save the first image if we find any.

## The Plan
Be sure to read the previous section if you're still confused as to what PyCuriosity is.

All great projects, big or small, always start with a plan. Planning out the project ahead of time saves confusion and 
provides a clear picture of the project, the resources to use, the skills to acquire and use. 

![Battle Plan GIF from Home Alone](https://cloud-odfqnnmkf-hack-club-bot.vercel.app/0giphy.gif)

This program flow was made using [diagrams.net](https://app.diagrams.net), be sure to check that out if you're planning
on making a big project, especially with a team.
![PyCuriosity program flow](https://cloud-2o6nek83e-hack-club-bot.vercel.app/0curiosity_battle_plan.png)

## Init
Fork the [starting repl](https://replit.com/@agentblack6000/pycuriosity-init?v=1). Let's see what we got-
- Right away you'll see a bunch of TODOs, incase you want to attempt the project solo
- Underneath the program/module docstring, you'll see a comment for imports. As mentioned earlier, we'll be using the
```requests``` module to make a GET request to the API and ```argparse``` to validate command line arguments. Add the
following imports using the [PEP-8 style guide](https://peps.python.org/pep-0008/#imports)
```python
import argparse

import requests
```
- Next, you'll see the ```main()``` and ```explore_mars_rover_photos(file_name, date)``` functions, also with a bunch of
TODOs, followed by this code snippet:
```python
if __name__ == "__main__":
    main()
```
If unfamiliar, this makes the program modular, so the functions defined can be used/imported in other projects.

### Initial setup
To access the Mars Rover Photos API, recall we need an API key. An API key is useful for authenticating data, so only
trusted parties with the right API key can request information, which is very useful if the data costs money to collect,
like weather data, population, etc. which might require paying for an API key. However, NASA's APIs are public and free,
so we don't really need to signup for an API key.

But, declaring an API key in a program is dangerous, as when code is visible to the public, everyone can copy-paste the API
key and make requests, accessing sensitive data, which isn't great if you had to pay for the API key, and may lead to
security breaches. As is convention, we export the API key as an environment variable in the terminal, and access it 
using the  builtin ```os``` module.
```python
...
import argparse
import os

import requests
...
```

Next, we need to access the API key, using the ```os``` module, using ```os.environ.get()```. See the documentation
[here](https://docs.python.org/3/library/os.html#file-names-command-line-arguments-and-environment-variables)
```python
import argparse
import os

import requests
...
API_KEY = os.environ.get("API_KEY")
...
```

To export the API key, click on Shell, next to Console, on replit

![Clicking on shell](https://cloud-fx418po7s-hack-club-bot.vercel.app/0shell.png)

If you signed up for an API key at [api.nasa.gov](https://api.nasa.gov/), copy it to your clipboard, and type in the 
following command
```shell
export API_KEY=your_api_key
```
If you didn't sign up for an API key, NASA allows using a demo key, which can be used by
```shell
export API_KEY=DEMO_KEY
```

### ```main()```
First, we need to check if the API key exists, and exit the program if the API key doesn't exist. This can be done
using the builtin ```sys``` module, with the ```sys.exit()``` function. See [documentation](https://python.readthedocs.io/en/latest/library/sys.html)
```python
...
import sys
...

def main():
    ...
    # Validate API key
    if not API_KEY:
        sys.exit("API Key not set")
    ...
```

#### Setting up ```argparse```
First, we need to look at the Mars Rover Photos API [documentation](https://github.com/corincerami/mars-photo-api), and 
look it up on [api.nasa.gov](https://api.nasa.gov/) as well. We'll be querying by Earth date to keep things simple.

After going through the documentation, the following parameters are necessary to include in the request-
1. The API key, which we've already gotten and validated
2. The Earth date(date Curiosity clicked the photos), which we need to get from the user

In addition to this, we also need to request a file name from the user to store the image URLs. Since we already 
have the API key from an environment variable, we need to accept a date and the file name from the user, using
```argparse```.

Before we start, read the ```argparse``` [documentation](https://docs.python.org/3/library/argparse.html).
We want to run the program in the following way-
```shell
python project.py -m file_name date
```
The reason for the -m flag is so we can expand the project later on, for example with other APIs, and this approach
makes it easy to add more command line arguments.

First, we need to sort out our imports, as per the PEP-8 style guide
```python
import os
import sys
from argparse import ArgumentParser

import requests
```
Since we need to use the ```ArgumentParser``` class, we'll just import that instead of the entire module.

Then, we need to configure ```argparse```, using the [documentation](https://docs.python.org/3/library/argparse.html)-
```python
import os
import sys
from argparse import ArgumentParser

import requests

def main():
    ...
    # Create argument parser and add optional command line arguments
    parser = ArgumentParser(description="A NASA API explorer that can get near Earth object data, "
                                        "Mars rover pictures, and the Astronomy "
                                        "Picture of the Day.")
    parser.add_argument("-m", "--mars", nargs=2, dest="mars", metavar=("file_name", "date"),
                        help="write the Mars rover image urls to a text file")

    # Parse arguments
    args = parser.parse_args()
```
The above code block first sets up the ```ArgumentParser``` as per the documentation(I've left out ```prog``` and 
```epilog``` for simplicity, feel free to add them, as well as modify existing keyword arguments as per the [docs](https://docs.python.org/3/library/argparse.html#argumentparser-objects)), and 
adds an argument flag (-m for Mars), which accepts 2 parameters or ```nargs```, stored in ```dest="mars"```, which we'll
use later on to validate the command line arguments, complete with ```metavar=("file_name", "date")``` for usage 
messages. The documentation for [```parser.add_argument()```](https://docs.python.org/3/library/argparse.html#the-add-argument-method)

## Finishing up
Link to the final source code-

[PyCuriosity Repl](https://replit.com/@agentblack6000/PyCuriosity?v=1)

