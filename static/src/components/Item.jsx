import React from 'react';
import './components.css'

export default class Item extends React.Component {

	constructor(props){
		super(props)
	}

  render () {
    return (
    	<div url={this.props.url} name={this.props.name} onClick={this.props.changeClicked} className="item">
    		{this.props.name}
    	</div>
    	);
  }
}