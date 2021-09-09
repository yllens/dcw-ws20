var http = require('http');
var fs = require('fs');
var querystring = require('querystring');
const port = 3022;

http.createServer(function (req, res) {
	let now = new Date();
    console.log(req.method + ": " + req.url)

    // Handle GET request
    if (req.method === "GET") {
        handleGetRequest(req, res);
    } else if (req.method === "POST") {
        handlePostRequest(req, res);
    }
    
}).listen(port);

console.log(`Server running at port ${port}...\nPress CTRL+C to stop.`);

function handleGetRequest(req, res) {
    // Check if file exists
    fs.stat(`.${req.url}`, function (err, stat) {

        if (err == null) {
            // File exists
            if (req.url === '/') {
                res.writeHead(200, { 'Content-Type': 'text/html; charset=UTF-8' });
                fs.createReadStream('html/index.html', 'UTF-8').pipe(res);
                return
            }

            if (req.url.endsWith('.css')) {
                res.writeHead(200, { 'Content-Type': 'text/css; charset=UTF-8' });
            } else if (req.url.endsWith('.html')) {
                res.writeHead(200, { 'Content-Type': 'text/html; charset=UTF-8' });
            } else if (req.url.endsWith('.js')) {
                res.writeHead(200, { 'Content-Type': 'application/javascript; charset=UTF-8' });
            }

            fs.createReadStream(`.${req.url}`, "UTF-8").pipe(res);

        } else if (err.code === 'ENOENT') {
            // File doesn't exist 
            response404_1(res);

        } else {
            console.log('unknown error');
            res.writeHead(500, { 'Content-Type': 'text/plain; charset=UTF-8' });
            res.end("Unknown error!");
        }
    });
}

function handlePostRequest(req, res) {
    var submitURLs = ["/submit-form-en-learner", "/submit-form-de-learner", "/submit-form-ru-learner",
     "/submit-form-en-assessor", "/submit-form-de-assessor", "/submit-form-ru-assessor"]
    // Handles request to /submit-form
    if (!submitURLs.includes(req.url)) {
        response404_2(res);
    } else {
        // Get data from submitted form
        var requestBody = ''
        req.on('data', chunk => {
            requestBody += chunk
        });
        
        // When all read, parse the data string to get form fields data
        req.on('end', () => {
            console.log(`requestBody: ${requestBody}\n`);
            var formData = querystring.parse(requestBody);
            console.log(formData);

            // Save the submitted data to JSON format
            writeToJson(req, formData);

            // Send form submitted response
            sendSuccessResponse(res);
        });
    }
}

function writeToJson(req, formData) {
    console.log(req.url);
    // Write to English learners json file
    if (req.url === '/submit-form-en-learner') {
        console.log(formData);
        fs.readFile('data/en/learnersDataEN.json', function (err, data) {
            var newKey;
            var jsonOutput = JSON.parse(data);

            // Get existing json length to generate a new unique key
            if (Object.keys(jsonOutput).length === 0) {
                newKey = "learner1";
            } else {
                newKey = "learner" + (Object.keys(jsonOutput).length + 1).toString();
            }
            // Append to json from existing file
            jsonOutput[newKey] = JSON.parse(JSON.stringify(formData));

            // Append new extended json to file
            fs.writeFileSync('data/en/learnersDataEN.json', JSON.stringify(jsonOutput));
        });
    // Write to German learners json file
    } else if (req.url === '/submit-form-de-learner') {
        fs.readFile('data/de/learnersDataDE.json', function (err, data) {
            var newKey;
            var jsonOutput = JSON.parse(data);
    
            // Get existing json length to generate a new unique key
            if (Object.keys(jsonOutput).length === 0) {
                newKey = "learner1";
            } else {
                newKey = "learner" + (Object.keys(jsonOutput).length + 1).toString();
            }
            // Append to json from existing file
            jsonOutput[newKey] = JSON.parse(JSON.stringify(formData));
            
            // Append new extended json to file
            fs.writeFileSync('data/de/learnersDataDE.json', JSON.stringify(jsonOutput));
        })
    // Write to Russian learners json file
    } else if (req.url === '/submit-form-ru-learner') {
        fs.readFile('data/ru/learnersDataRU.json', function (err, data) {
            var newKey;
            var jsonOutput = JSON.parse(data);
    
            // Get existing json length to generate a new unique key
            if (Object.keys(jsonOutput).length === 0) {
                newKey = "learner1";
            } else {
                newKey = "learner" + (Object.keys(jsonOutput).length + 1).toString();
            }
            // Append to json from existing file
            jsonOutput[newKey] = JSON.parse(JSON.stringify(formData));
            
            // Append new extended json to file
            fs.writeFileSync('data/ru/learnersDataRU.json', JSON.stringify(jsonOutput));
        })
    // Write to English assessors json file
    } else if (req.url === '/submit-form-en-assessor') {
        fs.readFile('data/en/assessorsDataEN.json', function (err, data) {
            var newKey;
            var jsonOutput = JSON.parse(data);
    
            // Get existing json length to generate a new unique key
            if (Object.keys(jsonOutput).length === 0) {
                newKey = "learner1";
            } else {
                newKey = "learner" + (Object.keys(jsonOutput).length + 1).toString();
            }
            // Append to json from existing file
            jsonOutput[newKey] = JSON.parse(JSON.stringify(formData));
            
            // Append new extended json to file
            fs.writeFileSync('data/en/assessorsDataEN.json', JSON.stringify(jsonOutput));
        })
    // Write to German assessors json file
    } else if (req.url === '/submit-form-de-assessor') {
        fs.readFile('data/de/assessorsDataDE.json', function (err, data) {
            var newKey;
            var jsonOutput = JSON.parse(data);
    
            // Get existing json length to generate a new unique key
            if (Object.keys(jsonOutput).length === 0) {
                newKey = "learner1";
            } else {
                newKey = "learner" + (Object.keys(jsonOutput).length + 1).toString();
            }
            // Append to json from existing file
            jsonOutput[newKey] = JSON.parse(JSON.stringify(formData));
            
            // Append new extended json to file
            fs.writeFileSync('data/de/assessorsDataDE.json', JSON.stringify(jsonOutput));
        })
    // Write to Russian assessors json file
    } else if (req.url === '/submit-form-ru-assessor') {
        fs.readFile('data/ru/assessorsDataRU.json', function (err, data) {
            var newKey;
            var jsonOutput = JSON.parse(data);
    
            // Get existing json length to generate a new unique key
            if (Object.keys(jsonOutput).length === 0) {
                newKey = "learner1";
            } else {
                newKey = "learner" + (Object.keys(jsonOutput).length + 1).toString();
            }
            // Append to json from existing file
            jsonOutput[newKey] = JSON.parse(JSON.stringify(formData));
            
            // Append new extended json to file
            fs.writeFileSync('data/ru/assessorsDataRU.json', JSON.stringify(jsonOutput));
        })
    } else {
        response404_2(res);
    }
}

function sendSuccessResponse(res) {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=UTF-8' });
    fs.createReadStream('./html/forms/form-submitted.html', "UTF-8").pipe(res);
}

function response404_1(res) {
    res.writeHead(404, { 'Content-Type': 'text/plain; charset=UTF-8' });
    res.end("Error with handleGetRequest: file not found.");
}

function response404_2(res) {
    res.writeHead(404, { 'Content-Type': 'text/plain; charset=UTF-8' });
    res.end("Error with handlePostrequest: file not found.");
}
