import React from 'react';

export default class URLField extends React.Component {

	constructor(props){
		super(props);
		
	}
  render () {
    return (
    	<div>
    		Input url
    		<input onChange={this.props.onChange} value={this.props.value} />
    		<button onClick={this.props.onClick}>parseURL</button>
    	</div>
    	);
  }
}