import React from 'react';
import './components.css'

export default class HTMLContent extends React.Component {

	constructor(props) {
		super(props);
	}

  render () {
  	var clear;
	if (this.props.innerHTML["__html"] == "")
	{
		clear = {
			opacity: 0,
			display: 'none',
			pointerEvents: 'none'
		}
	}
	else {
		clear = {
			opacity: 1,
		}
	}

    return (
    	<div className="innerHTML" style={clear}>
    		<div className="close" onClick={this.props.onClick}>
    		<img className="close-icon" src="/dist/icons/close_button.svg" />
    		</div>
    		<div  id="innerContent" dangerouslySetInnerHTML={this.props.innerHTML}>
    		</div>
    	</div>
    	);
  }
}