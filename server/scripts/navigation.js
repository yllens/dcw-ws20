
function validateForm() {
    var i, valid = true;
    
    var input = document.getElementsByClassName("req-field");
    var error = document.getElementsByClassName("invalid-feedback");

    // Check input field
    for (i = 0; i < input.length; i++) {
        if (input[i].value === "") {
            input[i].classList.add("is-invalid-select");
            error[i].style.display = "block";
            valid = false;
        }
    }
    return valid;
}

function openNextPage() {
	// Exit the function if any field in the current tab is invalid
	if (!validateForm()) return false;

	var typeInput = document.getElementById("type");
	var languageInput = document.getElementById("language");
	var testInput = document.getElementById("test");

	// Redirect to correct form
	if (typeInput.value === "learner") {
		if (languageInput.value === "en" && testInput.value === "en") {
			location.href = 'forms/en/learners/form-en-learner-en.html';
		} else if (languageInput.value === "en" && testInput.value === "de") {
			location.href = 'forms/en/learners/form-en-learner-de.html';
		} else if (languageInput.value === "en" && testInput.value === "ru") {
			location.href = 'forms/en/learners/form-en-learner-ru.html';

		} else if (languageInput.value === "de" && testInput.value === "en") {
			location.href = 'forms/de/learners/form-de-learner-en.html';
		} else if (languageInput.value === "de" && testInput.value === "de") {
			location.href = 'forms/de/learners/form-de-learner-de.html';
		} else if (languageInput.value === "de" && testInput.value === "ru"){
			location.href = 'forms/de/learners/form-de-learner-ru.html';

		} else if (languageInput.value === "ru" && testInput.value === "en") {
			location.href = 'forms/ru/learners/form-ru-learner-en.html';
		} else if (languageInput.value === "ru" && testInput.value === "de") {
			location.href = 'forms/ru/learners/form-ru-learner-de.html';
		} else if (languageInput.value === "ru" && testInput.value === "ru"){
			location.href = 'forms/ru/learners/form-ru-learner-ru.html';
		}
	} else if (typeInput.value === "assessor") {
		if (languageInput.value === "en" && testInput.value === "en") {
			location.href = 'forms/en/assessors/form-en-assessor-en.html';
		} else if (languageInput.value === "en" && testInput.value === "de") {
			location.href = 'forms/en/assessors/form-en-assessor-de.html';
		} else if (languageInput.value === "en" && testInput.value === "ru") {
			location.href = 'forms/en/assessors/form-en-assessor-ru.html';

		} else if (languageInput.value === "de" && testInput.value === "en") {
			location.href = 'forms/de/assessors/form-de-assessor-en.html';
		} else if (languageInput.value === "de" && testInput.value === "de") {
			location.href = 'forms/de/assessors/form-de-assessor-de.html';
		} else if (languageInput.value === "de" && testInput.value === "ru"){
			location.href = 'forms/de/assessors/form-de-assessor-ru.html';

		} else if (languageInput.value === "ru" && testInput.value === "en") {
			location.href = 'forms/ru/assessors/form-ru-assessor-en.html';
		} else if (languageInput.value === "ru" && testInput.value === "de") {
			location.href = 'forms/ru/assessors/form-ru-assessor-de.html';
		} else if (languageInput.value === "ru" && testInput.value === "ru"){
			location.href = 'forms/ru/assessors/form-ru-assessor-ru.html';
		}
	}
}

// Hide bootstrap required popups
document.addEventListener('invalid', (function () { 
    return function (e) {
        e.preventDefault();
        document.getElementById("tnc").focus();
    };
})(), true);

// Hide error message when input is edited
function hideErrorMsg() {
    document.getElementById("error").style.display = "none";
}