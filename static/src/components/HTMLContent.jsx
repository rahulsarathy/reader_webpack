import React from 'react';
import './components.css'

export default class HTMLContent extends React.Component {

	constructor(props) {
		super(props);
	}

  render () {
    return (
    	<div className="article" id="innerContent" dangerouslySetInnerHTML={this.props.innerHTML}>
    	</div>
    	);
  }
}