import React from 'react';
import './components.css';
import $ from 'jquery';

export default class Subscribe extends React.Component {

	constructor(props) {
		super(props);

	}

	render () {
		var text;
		var className;
		if (this.props.subscribe)
		{
			text = "subscribed"
			className = "subscribe light"
		}
		else {
			text = "subscribe"
			className="subscribe"
		}

		return (

			<div className={className} onClick={this.props.onClick}>
				{text}
			</div>
			);
	}
}