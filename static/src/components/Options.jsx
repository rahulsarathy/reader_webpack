import React from 'react';
import {Item, Categories} from './Components';
import $ from 'jquery';


var selected;
var columns;
var categories;

export default class Options extends React.Component {
	constructor(props) {
		super(props)

		this.subscribe = this.subscribe.bind(this)
		this.unsubscribe = this.unsubscribe.bind(this)

		this.state = {
			blogData: {},
			columnData: {}
		}
	}

	componentDidMount(){
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
					//var parsedColumns = this.parseColumns(data[1])
					this.setState(
						{
							blogData: data[1],
							columnData: data[0]
						});
				}.bind(this),
				error: function(xhr)
				{
					console.log("error is " + xhr)
				}
			});
	}


	createBlogs(){

		columns = {};

		for (var column in this.state.columnData)
		{
			columns[this.state.columnData[column]] = []
		}

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

			for (var category in blogData[key]['category'])
			{
				columns[blogData[key]['category'][category]].push(<Item name={key} onClick={this.props.onClick} subscribe={this.subscribe} unsubscribe={this.unsubscribe} selected={selected} changeClicked={this.props.changeClicked} display={display} />)
			}

		}
	}

	createColumns(){
		categories = []
		for (var key in columns)
		{
			categories.push(<Categories category={key} items={columns[key]}/>)
		}
	}

	render () {
		this.createBlogs();
		this.createColumns();
		return (
    		<div>
    		{categories}
   			</div>
    	);
  }
}