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
					console.log("error is " + xhr)
				}
			});
	}

	createBlogs(){

		blogs = [];

		var blogData = this.state.blogData;
		var toDisplay = blogData[0]
		for (var key in toDisplay)
		{
			var display = toDisplay[key]['display']
			blogs.push(<Item name={key} changeClicked={this.props.changeClicked} display={display} />);
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