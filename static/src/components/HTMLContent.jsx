import React from 'react';

export default class HTMLContent extends React.Component {

	constructor(props) {
		super(props);
	}

  render () {
    return (
    	<div id="innerContent">
    		{this.props.innerHTML}
    	</div>
    	);
  }
}