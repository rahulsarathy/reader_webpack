import React from 'react';
import {HTMLContent, ParseURL, URLField, Options, Reset, Poll} from './components/Components.jsx'
import $ from 'jquery';

export default class Reader extends React.Component {

	constructor(props) {
		super(props);

		this.showFirst = this.showFirst.bind(this);
		this.transition = this.transition.bind(this);

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

	transition(){
    	$(".bookview").toggleClass('active');
	}

	render () {
    return (
    	<div>
    	    <div className="bookview">
    			<Options onClick={this.transition} changeClicked={this.showFirst} showFirst={this.showFirst}/>
    		</div>
    		<Reset />
    		<Poll />
    		<HTMLContent innerHTML={this.state.innerHTML}/>
    	</div>
    	);
  }
}