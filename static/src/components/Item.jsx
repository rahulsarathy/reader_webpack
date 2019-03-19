import React from 'react';
import './components.css';

var toReturn;

export default class Item extends React.Component {

	constructor(props){
		super(props)
	}

  render () {
    var className;
    if (this.props.selected)
    {
      className="item-selected"
    }
    else {
      className="item-unselected"
    }
    return (
      <div name={this.props.name} onClick={this.props.changeClicked} className={className}>
        {this.props.display}
      </div>
    	);
    }
  }