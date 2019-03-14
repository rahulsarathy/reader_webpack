import React from 'react';
import {Item} from './Components';
import $ from 'jquery';


var blogs;

export default class Options extends React.Component {
	constructor(props) {
		super(props)
		this.state = {
			blogData: {}
		}
	}

	componentDidMount(){
		this.getBlogs();
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
					console.log(xhr)
				}
			});
	}

	createBlogs(){

		blogs = [];

		var blogData = this.state.blogData;
		for (var i = 0; i < blogData.length; i++)
		{
			blogs.push(<Item changeClicked={this.props.changeClicked} name={blogData[i]['display']} />);
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