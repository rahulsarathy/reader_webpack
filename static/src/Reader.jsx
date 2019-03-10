import React from 'react';
import {HTMLContent, ParseURL, URLField, Options} from './components/Components.jsx'
import $ from 'jquery';

export default class Reader extends React.Component {

	constructor(props) {
		super(props);

		this.handleChange = this.handleChange.bind(this);
		this.handleClick = this.handleClick.bind(this);
		this.showFirst = this.showFirst.bind(this);
		this.changeClicked = this.changeClicked.bind(this);

		this.state = {
			value: "",
			innerHTML: {
				__html: "<div></div>"
			},
			innerContent: '',
		};
	}

	handleChange(event) {
		this.setState(
			{
				value: event.target.value
			});
	}

	handleClick() {
		console.log("clicked");
		this.parseURL(this.state.value);
	}

	parseURL(url) {
	var data = {
		url: url
	}
	$.ajax(
		{ 
			type: "POST",
			url: '/retrieve', 
			dataType:'html',
			data: data, 
			success: function(data) 
			{ 
				console.log(data);
				this.setState(
					{
						innerHTML: {
							__html: data,
						},
					innerContent: data

					});
			}.bind(this),
			error: function(xhr)
			{
				console.log("errored");
				console.log(xhr.responseText)
				this.setState(
				{
					innerHTML: {
						__html: xhr.responseText,
						},
					innerContent: xhr.responseText

					});
			}.bind(this) 
		}
		);
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
    		<URLField value={this.state.value} onChange={this.handleChange} onClick={this.handleClick} />
    		<Options changeClicked={this.changeClicked} showFirst={this.showFirst}/>
    		<HTMLContent innerHTML={this.state.innerHTML}/>
    		<button onClick={this.showFirst}>Show First</button>
    	</div>
    	);
  }
}