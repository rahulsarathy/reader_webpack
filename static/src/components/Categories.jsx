import React from 'react';
import './components.css';
import {Item} from './Components';


export default class Categories extends React.Component {

	constructor(props){
		super(props)
	}

  render () {
   
    return (
      <div className="category">
        {this.props.category}
        {this.props.items}
      </div>
    	);
    }
  }