import React from 'react';
import ReactDOM from 'react-dom';
import Reader from "./Reader.jsx";
import Login from "./Login.jsx"
import $ from 'jquery';

const login = document.getElementById('login') !== null;
console.log("login is " + login)
if (login) {
	ReactDOM.render(< Login/>, document.getElementById('login'))
}

const content = document.getElementById('content') !== null;
console.log("content is " + content)
if (content) {
	const user_id = parseInt(document.getElementById('user_id').innerHTML)
	ReactDOM.render(< Reader user_id={user_id}/>, document.getElementById('content'))
}

$(document).ready(function() {
	//console.log("calling poll");
    // load the initial data (assuming it will be immediately available)
   // poll();
});