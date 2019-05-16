import React from 'react';
import $ from 'jquery';
import {Item, Categories} from './components/Components';

var blogs;

export default class Login extends React.Component {

	constructor(props) {
		super(props);

        this.state = {
            blogData: {}
        }
	}

    componentDidMount(){
        this.getBlogs();
    }

    createBlogs() {
        blogs = [];
        var blogData = this.state.blogData;

        for (var key in blogData)
        {
            var display = blogData[key]['display']
            var color = blogData[key]['color']
            var page = blogData[key]['page']
            blogs.push(<Item name={key} color={color} onClick={this.props.onClick} subscribe={this.subscribe} unsubscribe={this.unsubscribe} display={display} url={page} />);
        }

    }

    getBlogs() {
        $.ajax(
            {
                type: 'GET',
                url: '/blogs_no',
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

	render () {
    this.createBlogs();
    return (
        <div>
    	<div className="overlay"></div>
        <div className="blur">
            {blogs}
    	</div>
        </div>
    	);
  }
}