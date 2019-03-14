import React from 'react';
import './components.css';
import $ from 'jquery';

export default class Email extends React.Component {

	constructor(props) {
		super(props);

		this.send = this.send.bind(this);
	}

	send()
	{
		$.ajax(
			{
				type: 'POST',
				url: '/send'
			});
	}

	render () {
		return (
			<div>
				<button onClick={this.send}>Send</button>
			</div>
			);
	}
}