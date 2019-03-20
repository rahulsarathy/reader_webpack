import React from 'react';
import {HTMLContent, ParseURL, URLField, Options, Reset, Poll, Email} from './components/Components.jsx'
import $ from 'jquery';

export default class Reader extends React.Component {

	constructor(props) {
		super(props);

		this.showFirst = this.showFirst.bind(this);

		this.state = {
			innerHTML: {
				__html: "<div></div>"
			},
		};
	}


	showFirst(event)
	{
		var data = {
			name: event.target.parentNode.getAttribute('name')
		}
		$.ajax(
			{
				type: 'POST',
				url: '/parseRSS',
				dataType: 'html',
				data: data,
				success: function(data)
				{
					this.setState(
						{
							innerHTML: {
								__html: data
							} 
						});
				}.bind(this),
				error: function(xhr)
				{
					console.log("error is " + xhr.responseText)
				}
			});
	}

	render () {
    return (
    	<div>
    		<Options changeClicked={this.showFirst} showFirst={this.showFirst}/>
    		<Reset />
    		<Poll />
    		<Email />
    		<HTMLContent innerHTML={this.state.innerHTML}/>
    	</div>
    	);
  }
}