import React from 'react';
import ReactDOM from 'react-dom';
import Reader from "./Reader.jsx";
import Login from "./Login.jsx"
import User from "./User.jsx"
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

const user = document.getElementById('user') !== null;
console.log("user is " + user)
if (user) {
	ReactDOM.render(< User/>, document.getElementById('user'))
}

const register = document.getElementById('register') !== null;
console.log("user is " + register)
if (register) {
	ReactDOM.render(< Login/>, document.getElementById('register'))
}

$(document).ready(function() {
	//console.log("calling poll");
    // load the initial data (assuming it will be immediately available)
   // poll();
});