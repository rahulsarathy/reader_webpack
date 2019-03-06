import React from 'react';
import {HTMLContent, ParseURL, URLField, Options} from './components/Components.jsx'
import $ from 'jquery';

export default class Reader extends React.Component {

	constructor(props) {
		super(props);

		this.handleChange = this.handleChange.bind(this);
		this.handleClick = this.handleClick.bind(this);


		this.state = {
			value: "",
			innerHTML: {
				__html: "<div></div>"
			},
			innerContent: ''
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

	render () {
    return (
    	<div>
    		<URLField value={this.state.value} onChange={this.handleChange} onClick={this.handleClick} />
    		<Options />
    		<HTMLContent innerHTML={this.state.innerContent}/>
    	</div>
    	);
  }
}