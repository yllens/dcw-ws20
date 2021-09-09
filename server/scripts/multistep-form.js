// Author: 			yllens
// Last modified: 	24.04.2021
// Modified from https://www.w3schools.com/howto/howto_js_form_steps.asp

var currentTab = 0;   // Current tab is set to be the first tab (0)
showTab(currentTab);  // Display the current tab

// Display the current form tab
function showTab(n) { 
	var tab = document.getElementsByClassName("tab");
	tab[n].style.display = "block";

	if (n == 0) {
		// Hide 'Previous' button on first tab
		document.getElementById("prevButton").style.display = "none";
	} else {
		// If not first tab, show 'Previous' button
		document.getElementById("prevButton").style.display = "inline";
	}
	if (n == (tab.length-1)) {
		// If final tab, 'Next' button is a submit button
		document.getElementById("nextButton").value = "Submit";
	} else {
		// Else 'Next' button takes user to next tab
		document.getElementById("nextButton").value = "→";
	}

	// Display the correct step indicator
	fixStepIndicator(n)
}

// Determine which tab to display
function nextTab(n) {
	var tab = document.getElementsByClassName("tab");

	// Exit the function if any field in the current tab is invalid
	if (n == 1 && !validateForm()) return false;

	// Hide current tab
	tab[currentTab].style.display = "none";

	// Increase or decrease the current tab by 1
	currentTab = currentTab + n;

	// If end of the form, submit
	if (currentTab >= tab.length) {
		document.getElementById("nextButton").type = "submit";
		return false;
	}

	// Else, display the correct tab:
	showTab(currentTab);
}

// Validate form fields
function validateForm() {
	var tab, i, error, valid = true;
	tab = document.getElementsByClassName("tab");
	input = tab[currentTab].getElementsByClassName("req-field");
	error = document.getElementById("error");
    
	// Check every input field in the current tab
	for (i = 0; i < input.length; i++) {
		if (input[i].type === "checkbox") {
			if (input[i].checked === false) {
				input[i].className += " is-invalid";
				error.style.display = "block";
				valid = false;
			}
		} else if (input[i].type === "radio") {
			if (input[i].checked === false) {
				input[i].className += " is-invalid-select";
				error.style.display = "block";
				valid = false;
			}
		} else if (input[i].type === "select-one") {
			if (input[i].value === "") {
				input[i].className += " is-invalid-select";
				error.style.display = "block";
				valid = false;
			}
		} else {
			if (input[i].value === "") {
				input[i].className += " is-invalid";
				error.style.display = "block";
				valid = false;
			}
		}
	}
	// If the valid status is true, mark step as finished and valid
	if (valid) {
		document.getElementsByClassName("formStep")[currentTab].className += " finish";
	}
	return valid;
}

// Removes "active" class of all steps
function fixStepIndicator(n) {
	var i, tab = document.getElementsByClassName("formStep");

	for (i = 0; i < tab.length; i++) {
		tab[i].className = tab[i].className.replace(" active", "");
	}

	tab[n].className += " active";
  }

// Show additional questions if assessor is also a language teacher
function showTeachingQuestions() {
	var selectField = document.getElementById('hiddenSelect');
	var hiddenFieldsTeachersDiv = document.getElementsByClassName('hidden-input-teacher-div');
	var hiddenFieldsAssessorsDiv = document.getElementById('hidden-input-assessor-div');

	// var hiddenFieldsTeachersField = document.getElementsByClassName('hidden-input-teacher-field');
	// var hiddenFieldsAssessorsField = document.getElementsByClassName('hidden-input-assessor-field');
	
	if (selectField.value === 'yes') {
		for (var i=0; i<hiddenFieldsTeachersDiv.length; i++) {
			hiddenFieldsTeachersDiv[i].style.display = 'block';
			// hiddenFieldsTeachersField[i].classList += 'req-field';
		}
		hiddenFieldsAssessorsDiv.style.display = 'none';
	
	} else if (selectField.value === 'no') {
		// hiddenFieldsAssessorsField.classList.add('test');
		hiddenFieldsAssessorsDiv.style.display = 'block';

		for (var i=0; i<hiddenFieldsTeachersDiv.length; i++) {
			hiddenFieldsTeachersDiv[i].style.display = 'none';
		}
	}
}

// Hide error message when input is edited
function hideErrorMsg() {
    document.getElementById('error').style.display = 'none';
}

// Hide bootstrap required popups
document.addEventListener('invalid', (function () { 
    return function (e) {
        e.preventDefault();
        document.getElementById("tnc").focus();
    };
})(), true);