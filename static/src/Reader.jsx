import React from 'react';
import {HTMLContent, ParseURL, URLField, Options} from './components/Components.jsx'
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
		console.log("clicked");
		this.parseURL(this.state.value);
	}

	

	showFirst(data)
	{
		console.log()
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
		console.log(event.target);
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
    	</div>
    	);
  }
}