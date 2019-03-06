import React from 'react';
import ReactDOM from 'react-dom';
import Reader from "./Reader.jsx";
import $ from 'jquery';

ReactDOM.render(<Reader />, document.getElementById("content"));

function poll() {
	$.ajax(
		{
			type: 'POST',
			url: '/poll',
		});
}

$(document).ready(function() {
	//console.log("calling poll");
    // load the initial data (assuming it will be immediately available)
   // poll();
});

