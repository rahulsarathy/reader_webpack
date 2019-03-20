import React from 'react';
import {Item} from './Components';
import $ from 'jquery';


var blogs;
var selected;

export default class Options extends React.Component {
	constructor(props) {
		super(props)

		this.subscribe = this.subscribe.bind(this)
		this.unsubscribe = this.unsubscribe.bind(this)

		this.state = {
			blogData: {}
		}
	}

	componentDidMount(){
		console.log("Called")
		this.getBlogs();
	}


	subscribe(e)
	{
		var data = {
			name: event.target.parentNode.getAttribute('name')
		}
		$.ajax(
			{
				type: 'POST',
				url: '/subscribe',
				data: data
			});

	}

	unsubscribe(e)
	{
		var data = {
			name: event.target.parentNode.getAttribute('name')
		}
		$.ajax(
			{
				type: 'POST',
				url: '/unsubscribe',
				data: data
			});

	}

	getBlogs() {
		$.ajax(
			{
				type: 'GET',
				url: '/blogs',
				dataType: 'json',
				success: function(data)
				{
					this.setState(
						{
							blogData: data
						});
				}.bind(this),
				error: function(xhr)
				{
					console.log("error is " + xhr)
				}
			});
	}

	createBlogs(){

		blogs = [];

		var blogData = this.state.blogData;
		for (var key in blogData)
		{
			var display = blogData[key]['display']
			var selected;
			if (blogData[key].hasOwnProperty('selected'))
			{
				if (blogData[key]['selected'])
				{
					selected = true;
				}
				else {
					selected = false;
				}

			}
			else {
				selected = false;
			}
			blogs.push(<Item name={key} subscribe={this.subscribe} unsubscribe={this.unsubscribe} selected={selected} changeClicked={this.props.changeClicked} display={display} />);
		}
	}

	render () {
		this.createBlogs();
		return (
    		<div>
    			{blogs}
    		</div>
    	);
  }
}