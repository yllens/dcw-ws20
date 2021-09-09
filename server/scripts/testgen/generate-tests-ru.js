// Modified from https://www.sitepoint.com/simple-javascript-quiz/ and https://stackoverflow.com/questions/40201137/i-need-to-read-a-text-file-from-a-javascript

const testContainer = document.getElementById('gapTest');

var textsArray = []; var pageOutput = [];

(function () {
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

            textsArray.forEach(function (currentText) {
                pageOutput.push(`<div class="tab"><h4>Текст ${counter}</h4>`);
                if (counter !== 1) {
                    pageOutput.push("<p>Пожалуйста, заполните пробелы:</p>")
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
                <h6>Вопрос  1</h6>
                <p>Насколько легко читать этот текст?</p>
                <div class="form-group row mb-2">
                    <fieldset class="req" id="readingEaseT${counter}" required>
                        <div class="text-center">
                            <div class="form-check-inline text-center">
                                <input class="form-check-input" name="readingEaseT${counter}" value="very easy" id="very easy" type="radio"/><br/>
                                <label class="form-check-label">Очень легко</label>
                            </div>

                            <div class="form-check-inline text-center">
                                <input class="form-check-input" name="readingEaseT${counter}" value="easy" id="easy" type="radio"/><br/>
                                <label class="form-check-label">Легко</label>
                            </div>

                            <div class="form-check-inline text-center">
                                <input class="form-check-input" name="readingEaseT${counter}" value="fairly easy" id="fairly easy" type="radio"/><br/>
                                <label class="form-check-label">Довольно легко</label>
                            </div>

                            <div class="form-check-inline text-center">
                                <input class="form-check-input" name="readingEaseT${counter}" value="standard" id="standard" type="radio"/><br/>
                                <label class="form-check-label">Обычно</label>
                            </div>

                            <div class="form-check-inline text-center">
                                <input class="form-check-input" name="readingEaseT${counter}" value="fairly difficult" id="fairly difficult" type="radio"/><br/>
                                <label class="form-check-label">Довольно трудно</label>
                            </div>

                            <div class="form-check-inline text-center">
                                <input class="form-check-input" name="readingEaseT${counter}" value="difficult" id="difficult" type="radio"/><br/>
                                <label class="form-check-label">Трудно</label>
                            </div>

                            <div class="form-check-inline text-center">
                                <input class="form-check-input" name="readingEaseT${counter}" value="very difficult" id="very difficult" type="radio"/><br/>
                                <label class="form-check-label">Очень трудно</label>
                            </div>
                        </div>
                    </fieldset>
                </div>
                </br></br>
                <h6>Вопрос 2</h6>
                <p>Как часто в тексте вам встречались сложные слова?</p>
                <div class="form-group row mb-2">
                    <fieldset class="req" id="difficultWordsT${counter}" required>
                        <div class="text-center">
                            <div class="form-check-inline text-center">
                                <input class="form-check-input" name="difficultWordsT${counter}" value="never" id="never" type="radio"/><br/>
                                <label class="form-check-label" for="never">Никогда</label>
                            </div>

                            <div class="form-check-inline text-center">
                                <input class="form-check-input" name="difficultWordsT${counter}" value="very rarely" id="very rarely" type="radio"/><br/>
                                <label class="form-check-label">Очень редко</label>
                            </div>

                            <div class="form-check-inline text-center">
                                <input class="form-check-input" name="difficultWordsT${counter}" value="rarely" id="rarely" type="radio"/><br/>
                                <label class="form-check-label">Редко</label>
                            </div>

                            <div class="form-check-inline text-center">
                                <input class="form-check-input" name="difficultWordsT${counter}" value="occasionally" id="occasionally" type="radio"/><br/>
                                <label class="form-check-label">Время от времени</label>
                            </div>

                            <div class="form-check-inline text-center">
                                <input class="form-check-input" name="difficultWordsT${counter}" value="frequently" id="frequently" type="radio"/><br/>
                                <label class="form-check-label">Часто</label>
                            </div>

                            <div class="form-check-inline text-center">
                                <input class="form-check-input" name="difficultWordsT${counter}" value="very frequently" id="very frequently" type="radio"/><br/>
                                <label class="form-check-label">Очень часто</label>
                            </div>

                        </div>
                    </fieldset>
                </div>
                </br></br>
                <h6>Вопрос 3</h6>
                <p>Какие слова вам показались трудными?</p>
                <div class="form-group row mb-2">
                    <div class="class="form-group row mb-2>
                        <textarea class="col-sm-4" name="difficultWordsCommentT${counter}"
                            placeholder="Дополнительный комментарий здесь ..."></textarea>
                    </div>
                </div>
                </br></br>
                <h6>Вопрос 4</h6>
                <p>Имеются ли у вас еще какие-либо комментарии?</p>
                <div class="form-group row mb-2">
                    <div class="class="form-group row mb-2>
                        <textarea class="col-sm-4" name="commentT${counter}"
                            placeholder="Дополнительный комментарий здесь ..."></textarea>
                    </div>
                </div>`)
                pageOutput.push('</div>');
                counter++;
            });

            // Merge punctuation with the correct token
            var newPageOutput = [];
            var punct = ['.', ','];
            pageOutput.forEach(function (item) {
                // console.log(item);
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

    getTextsFromJson('ru');

})();
