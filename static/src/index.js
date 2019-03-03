import _ from 'lodash';

function component() {
  let element = document.createElement('div');

  // Lodash, currently included via a script, is required for this line to work
  element.innerHTML = _.join(['Hello', 'webpack', 'blah3']);
  element.id = "demo";
  return element;
}

function parse() {
	let element = document.createElement('BUTTON');

	element.innerHTML = 'parse';
	element.onclick = callParse;
	return element;
}

function callParse() {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function () {
		if (this.readyState == 4 && this.status == 200) {
			document.getElementById("demo").innerHTML = this.responseText;
		}
	};
	xhttp.open("POST", "/parse", true);
	xhttp.send();
}

document.body.appendChild(component());
document.body.appendChild(parse());