import React from 'react';
import {Item, Categories} from './Components';
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
		var name = event.target.parentNode.getAttribute('name');

		var blogData = this.state.blogData;
		blogData[name]['selected'] = true;
		var data = {
			name: name
		}
		$.ajax(
			{
				type: 'POST',
				url: '/subscribe',
				data: data
			});
		this.setState(
			{
				blogData: blogData
			});

	}

	unsubscribe(e)
	{
		var name = event.target.parentNode.getAttribute('name');
		var blogData = this.state.blogData;
		blogData[name]['selected'] = false;
		var data = {
			name: name
		}
		$.ajax(
			{
				type: 'POST',
				url: '/unsubscribe',
				data: data
			});
		this.setState(
		{
			blogData: blogData
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
			var color = blogData[key]['color']
			var page = blogData[key]['page']

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
			console.log(blogData[key]['image'])
			blogs.push(<Item name={key} color={color} onClick={this.props.onClick} subscribe={this.subscribe} unsubscribe={this.unsubscribe} selected={selected} changeClicked={this.props.changeClicked} display={display} url={page} />);
		}
	}

	render () {
		this.createBlogs();
		return (
    		<div style={this.props.blur}>
    			{blogs}
    		</div>
    	);
  }
}