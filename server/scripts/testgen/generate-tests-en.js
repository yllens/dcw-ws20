// Author:        yllens
// Last modified: 9.09.2021

// Div element containing the gapTest container tab
const testContainer = document.getElementById('gapTest');

// Array containing data from the JSON testlet files
var textsArray = [];

// Array containing data to format into HTML which is then pushed into the gapTest div test container
var pageOutput = [];

 // The getTextsFromJson and handleFileData are modified from https://stackoverflow.com/questions/40201137/i-need-to-read-a-text-file-from-a-javascript
(function () {
    // Read in input text JSON file
    function getTextsFromJson(language) {
        function readFileFromServer(path, callback) {
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function () {
                if (xhr.readyState == 4) {
                    if (xhr.status == 200) {
                        callback(xhr.responseText);
                    } else {
                        callback(null);
                    }
                }
            };
            xhr.open("GET", path);
            xhr.send();
        }

        // Parse input file
        function handleFileData(fileData) {
            if (!fileData) {
                return;
            }
            var jsonTexts = JSON.parse(fileData);

            for (var i = 0; i < jsonTexts.length; i++) {
                var currText = jsonTexts[i];
                textsArray.push(currText);
            }

            var counter = 1;

            // Generate form tab containing the test data (modified from https://www.sitepoint.com/simple-javascript-quiz/)
            textsArray.forEach(function (currentText) {
                pageOutput.push(`<div class="tab"><h4>Text ${counter}</h4>`);
                if (counter !== 1) {
                    pageOutput.push("<p>Please fill in the gaps:</p>")
                }
                pageOutput.push(`<div class="text-group">`);
                for (var i = 0; i < currentText.length; i++) {
                    if (currentText[i].gap === false) {
                        pageOutput.push(currentText[i].token);
                    } else {
                        pageOutput.push(
                            `<label>
                                    ${currentText[i].token}<input type="text" class="gap-field" spellcheck="false" autocomplete="off" autocorrect="off" autocapitalize="off" name="${currentText[i].gap_id}">
                            </label>
                            `
                        );
                    }
                }
                pageOutput.push(`</div>`)
                pageOutput.push(`
                </br></br></br>
                <h6>Question 1</h6>
                <p>How easy is this text to read?</p>
                <div class="form-group row mb-2">
                    <fieldset class="req" id="readingEaseT${counter}" required>
                        <div class="text-center">
                            <div class="form-check-inline text-center">
                                <input class="form-check-input" name="readingEaseT${counter}" value="very easy" id="very easy" type="radio"/><br/>
                                <label class="form-check-label">Very easy</label>
                            </div>

                            <div class="form-check-inline text-center">
                                <input class="form-check-input" name="readingEaseT${counter}" value="easy" id="easy" type="radio"/><br/>
                                <label class="form-check-label">Easy</label>
                            </div>

                            <div class="form-check-inline text-center">
                                <input class="form-check-input" name="readingEaseT${counter}" value="fairly easy" id="fairly easy" type="radio"/><br/>
                                <label class="form-check-label">Fairly easy</label>
                            </div>

                            <div class="form-check-inline text-center">
                                <input class="form-check-input" name="readingEaseT${counter}" value="standard" id="standard" type="radio"/><br/>
                                <label class="form-check-label">Standard</label>
                            </div>

                            <div class="form-check-inline text-center">
                                <input class="form-check-input" name="readingEaseT${counter}" value="fairly difficult" id="fairly difficult" type="radio"/><br/>
                                <label class="form-check-label">Fairly difficult</label>
                            </div>

                            <div class="form-check-inline text-center">
                                <input class="form-check-input" name="readingEaseT${counter}" value="difficult" id="difficult" type="radio"/><br/>
                                <label class="form-check-label">Difficult</label>
                            </div>

                            <div class="form-check-inline text-center">
                                <input class="form-check-input" name="readingEaseT${counter}" value="very difficult" id="very difficult" type="radio"/><br/>
                                <label class="form-check-label">Very difficult</label>
                            </div>
                        </div>
                    </fieldset>
                </div>
                </br></br>
                <h6>Question 2</h6>
                <p>How often did you find there to be difficult words?</p>
                <div class="form-group row mb-2">
                    <fieldset class="req" id="difficultWordsT${counter}" required>
                        <div class="text-center">
                            <div class="form-check-inline text-center">
                                <input class="form-check-input" name="difficultWordsT${counter}" value="never" id="never" type="radio"/><br/>
                                <label class="form-check-label" for="never">Never</label>
                            </div>

                            <div class="form-check-inline text-center">
                                <input class="form-check-input" name="difficultWordsT${counter}" value="very rarely" id="very rarely" type="radio"/><br/>
                                <label class="form-check-label">Very rarely</label>
                            </div>

                            <div class="form-check-inline text-center">
                                <input class="form-check-input" name="difficultWordsT${counter}" value="rarely" id="rarely" type="radio"/><br/>
                                <label class="form-check-label">Rarely</label>
                            </div>

                            <div class="form-check-inline text-center">
                                <input class="form-check-input" name="difficultWordsT${counter}" value="occasionally" id="occasionally" type="radio"/><br/>
                                <label class="form-check-label">Occasionally</label>
                            </div>

                            <div class="form-check-inline text-center">
                                <input class="form-check-input" name="difficultWordsT${counter}" value="frequently" id="frequently" type="radio"/><br/>
                                <label class="form-check-label">Frequently</label>
                            </div>

                            <div class="form-check-inline text-center">
                                <input class="form-check-input" name="difficultWordsT${counter}" value="very frequently" id="very frequently" type="radio"/><br/>
                                <label class="form-check-label">Very frequently</label>
                            </div>

                        </div>
                    </fieldset>
                </div>
                </br></br>
                <h6>Question 3</h6>
                <p>Which words did you find difficult?</p>
                <div class="form-group row mb-2">
                    <div class="class="form-group row mb-2>
                        <textarea class="col-sm-4" name="difficultWordsCommentT${counter}"
                            placeholder="Optional comment here ..."></textarea>
                    </div>
                </div>
                </br></br>
                <h6>Question 4</h6>
                <p>Do you have any other comments?</p>
                <div class="form-group row mb-2">
                    <div class="class="form-group row mb-2>
                        <textarea class="col-sm-4" name="commentT${counter}"
                            placeholder="Optional comment here ..."></textarea>
                    </div>
                </div>`)
                pageOutput.push('</div>');
                counter++;
            });

            // Merge punctuation with the correct token
            var newPageOutput = [];
            var punct = ['.', ','];
            pageOutput.forEach(function (item) {
                if (punct.includes(item)) {
                    var old = newPageOutput.pop();
                    newPageOutput.push(old + item);
                } else {
                    newPageOutput.push(item);
                }
            });
            
            testContainer.innerHTML = newPageOutput.join(" ");
        }
        readFileFromServer(`../../../../texts/${language}/${language}-standard.json`, handleFileData);
    }

    getTextsFromJson('en');

})();
