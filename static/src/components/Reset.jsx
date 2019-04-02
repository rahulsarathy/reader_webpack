import React from 'react';
import './components.css';
import $ from 'jquery';

export default class Reset extends React.Component {

	constructor(props) {
		super(props);

		this.reset = this.reset.bind(this);
	}

	reset()
	{
		$.ajax(
			{
				type: 'POST',
				url: '/reset'
			});
	}

	render () {
		return (
			<div>
				<button onClick={this.reset}>Reset</button>
			</div>
			);
	}
}