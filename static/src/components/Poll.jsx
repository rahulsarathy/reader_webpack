import React from 'react';
import './components.css';
import $ from 'jquery';

export default class Polling extends React.Component {

	constructor(props) {
		super(props);

		this.poll = this.poll.bind(this);
		this.send = this.send.bind(this);

	}

	poll()
	{
		$.ajax(
			{
				type: 'POST',
				url: '/poll'
			});
	}

	send(){
		$.ajax(
		{
			type: 'POST',
			url: '/send'
		})
	}

	render () {
		return (
			<div>
				<button onClick={this.poll}>Poll</button>
				<button onClick={this.send}>Send Email</button>
			</div>
			);
	}
}