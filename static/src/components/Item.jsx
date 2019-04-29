import React from 'react';
import './components.css';
import {Subscribe} from './Components.jsx'


var toReturn;

export default class Item extends React.Component {

	constructor(props){
		super(props)
	}

  render () {
    var className;
    var subButton;

    if (this.props.selected)
    {
      className="item selected"
      subButton = <Subscribe onClick={this.props.unsubscribe} subscribe={true}/>

    }
    else {
      className="item unselected"
      subButton = <Subscribe onClick={this.props.subscribe} subscribe={false}/>
    }


    return (
      <div className="item-wrapper" name={this.props.name}>
        <div onClick={this.props.changeClicked} style={{backgroundColor: this.props.color}} className={className}>
          <button onClick={this.props.changeClicked} >Get HTML</button>
          <img className="blogImage" src={"/dist/images/" + this.props.name + ".png"} />
          <p className="itemtext">{this.props.display}</p>
          {/*
          <a className="page" href={this.props.url} > Visit website</a>
        */}
        </div>
        {subButton}
      </div>
    	);
    }
  }