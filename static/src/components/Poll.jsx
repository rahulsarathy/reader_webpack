import React from 'react';
import './components.css';
import $ from 'jquery';

export default class Polling extends React.Component {

	constructor(props) {
		super(props);

		this.poll = this.poll.bind(this);
	}

	poll()
	{
		$.ajax(
			{
				type: 'POST',
				url: '/poll'
			});
	}

	render () {
		return (
			<div>
				<button onClick={this.poll}>Poll</button>
			</div>
			);
	}
}