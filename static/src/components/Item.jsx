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
      className="item selected"
    }
    else {
      className="item unselected"
    }
    return (
      <div name={this.props.name} className={className}>
        <button onClick={this.props.subscribe}>Subscribe</button>
        <button onClick={this.props.unsubscribe}>Unsubscribe</button>
        <button onClick={this.props.changeClicked} >Get HTML</button>
        <button onClick={this.props.onClick}>transition</button>
        <p className="itemtext">{this.props.display}</p>
      </div>
    	);
    }
  }