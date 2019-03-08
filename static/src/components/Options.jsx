import React from 'react';
import {Item} from './Components';

var blogs;

var data = [
	{
		name: "stratechery",
		url: "https://stratechery.com/feed"
	},
	{
		name: "startupboy",
		url: "https://startupboy.com/feed"
	},
	{
		name: "Bryan Caplan Econlib",
		url: "https://www.econlib.org/feed/indexCaplan_xml"
	},
	{
		name: "Marginal Revolution",
		url: "https://feeds.feedburner.com/marginalrevolution/"
	},
	{
		name: "Ribbon Farm",
		url: "https://ribbonfarm.com/feed"
	},
	{
		name: "Melting Asphalt",
		url: "https://meltingasphalt.com/feed/"

	}
];

var names = ["startupboy", 
"less wrong", 
"ribbon farm", 
"stratechery", 
"melting asphalt",
"overcoming bias",
"econlib",
"marginal revolution",
"elaine ou",
"devon zuegel",
"andrew kortina",
"eugene wei",
"paul graham",
"ben evans",
"above the crowd",
"Scott Adams blog",
"andrew chen",
"tony sheng",
"vital buterin",
"Conversations with tyler",
"Gwern"]



export default class Options extends React.Component {
	constructor(props) {
		super(props)
		this.createBlogs()
	}

	createBlogs(){
		blogs = data.map((blog) =>
			<Item changeClicked={this.props.changeClicked} name={blog["name"]} url={blog["url"]} />
		);
	}

	render () {

		return (
    		<div>
    			{blogs}
    		</div>
    	);
  }
}