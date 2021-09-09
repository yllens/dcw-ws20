# Data Collection on the Web WS 2020-21

This repository contains all of the front end and back end files for the Data Collection WS 2020-21 project.

## Client and server side

The `server` directory is the front-end containing all of the JavaScript and HTML code, as well as the input text files for generating C-tests on the webpage in the `texts` directory and the JSON files for saving the form output in the `data` directory.

Usage instructions:

* cd into the `server` directory containing the `start-server` script
* run `node start-server.js` (note: this code was developed and tested using Node.js v15.14.0)
* homepage: http://localhost:3022/html/index.html

## Additional scripts (Backend)

The `gapper` directory contains the Python code used to generate the JSON files containing C-tests.
It also offers the option to run a linguistic complexity analysis. Note that DataAnalysis.py is a draft and not finalised.

Usage instruction:

* use main.py by specifying the arguments required according to the documention of the main() function

