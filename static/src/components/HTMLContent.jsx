import React from 'react';

export default class HTMLContent extends React.Component {

	constructor(props) {
		super(props);
	}

  render () {
    return (
    	<div id="innerContent" dangerouslySetInnerHTML={this.props.innerHTML}>
    	</div>
    	);
  }
}