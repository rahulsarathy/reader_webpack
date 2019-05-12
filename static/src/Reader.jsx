import React from 'react';
import {HTMLContent, ParseURL, URLField, Options, Reset, Poll} from './components/Components.jsx'
import $ from 'jquery';

export default class Reader extends React.Component {

	constructor(props) {
		super(props);

		this.showFirst = this.showFirst.bind(this);
		this.closeHTML = this.closeHTML.bind(this);

		this.state = {
			closed: true,
			innerHTML: {
				__html: ""
			},
		};
	}


	showFirst(event)
	{
		event.persist()
		this.setState(
			{
				closed: false,
				innerHTML: {
					__html: "Loading..."
				}
			},
			() => 
			{
				this.showFirstCallback(event)
			}
			);
	}

	showFirstCallback(event)
	{
		console.log(event.target)
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
					if (!this.state.closed)
					{
						this.setState({
							innerHTML: {
								__html: data
							} 
						});
					}
				}.bind(this),
				error: function(xhr)
				{
					console.log("error is " + xhr.responseText)
				}
			});
	}

	closeHTML(){

		this.setState({
			closed: true,
			innerHTML: {
				__html: ""
			}
		})
	}


	render () {

	var blur

	if (this.state.innerHTML["__html"] == "")
	{
		blur = {
			
		}
	}
	else {
		blur = {
			filter: 'blur(20px)'
		}
	}

    return (
    	<div className="reader">
    		<HTMLContent innerHTML={this.state.innerHTML} onClick={this.closeHTML} />
    		<Options onClick={this.transition} changeClicked={this.showFirst} blur={blur} />
    	</div>
    	);
  }
}