import _ from 'lodash';
import $ from 'jquery';
import React from 'react';
import ReactDOM from 'react-dom';
import App from "./App.jsx";


window.jQuery = $;
window.$ = $;

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

function urlButton() {
	let element = document.createElement('BUTTON');
	element.id="urlButton"
	element.innerHTML = 'parseURL'
	element.onclick = parseURL;
	return element
}

function callParse() {
	var xhttp = new XMLHttpRequest();
	var textInput = document.getElementById("textBox").value;
	var data = new FormData();
	data.append('html', textInput);

	console.log("textInput is " + data);

	xhttp.onreadystatechange = function () {
		if (this.readyState == 4 && this.status == 200) {
			document.getElementById("demo").innerHTML = this.responseText;
		}
	};
	xhttp.open("POST", "/parse", true);
	xhttp.send(data);
}

function parseURL() {
	var url = document.getElementById("textBox").value;
	var data = {
		url: url
	}
	$.ajax(
		{ 
			type: "POST",
			url: '/retrieve', 
			dataType:'jsonp',
			data: data, 
			success: function(data) 
			{ 
				console.log(data);
			},
			error: function(xhr)
			{
				console.log(xhr.responseText)
			} 
		});
}


function input() {
	var textBox = document.createElement("INPUT");
	textBox.id = "textBox";
	textBox.setAttribute("type", "text");
	textBox.setAttribute("value", "");

	return textBox;
}

document.body.appendChild(component());
document.body.appendChild(parse());
document.body.appendChild(input());
document.body.appendChild(urlButton());

ReactDOM.render(<App />, document.getElementById("content"));
