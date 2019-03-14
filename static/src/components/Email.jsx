import React from 'react';
import './components.css';
import $ from 'jquery';

export default class Email extends React.Component {

	constructor(props) {
		super(props);

		this.send = this.send.bind(this);
		this.handleChange = this.handleChange.bind(this);
		this.state = {
			value: ""
		};
	}

	send()
	{
		var data = {
			recipient: this.state.value
		}
		$.ajax(
			{
				data: data,
				url: '/send'
			});
	}

	handleChange(event) {
		this.setState(
			{
				value: event.target.value
			});
	}

	render () {
		return (
			<div>
				<input onChange={this.handleChange} type="text" value={this.state.value} />
				<button onClick={this.send}>Send</button>
			</div>
			);
	}
}