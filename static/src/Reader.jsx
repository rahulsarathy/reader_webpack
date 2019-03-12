import React from 'react';
import {HTMLContent, ParseURL, URLField, Options, Reset, Poll} from './components/Components.jsx'
import $ from 'jquery';

export default class Reader extends React.Component {

	constructor(props) {
		super(props);

		this.showFirst = this.showFirst.bind(this);
		this.changeClicked = this.changeClicked.bind(this);

		this.state = {
			innerHTML: {
				__html: "<div></div>"
			},
			innerContent: '',
		};
	}

	handleClick() {
		this.parseURL(this.state.value);
	}

	

	showFirst(data)
	{
		$.ajax(
			{
				type: 'POST',
				url: '/first',
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
					console.log(xhr.responseText)
				}
			});
	}

	changeClicked(event) {
		var data = {
			url: event.target.getAttribute('url'),
			name: event.target.getAttribute('name')
		}
		this.showFirst(data);
	}

	render () {
    return (
    	<div>
    		<Options changeClicked={this.changeClicked} showFirst={this.showFirst}/>
    		<HTMLContent innerHTML={this.state.innerHTML}/>
    		<Reset />
    		<Poll />
    	</div>
    	);
  }
}