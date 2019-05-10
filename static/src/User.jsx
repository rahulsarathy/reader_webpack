import React from 'react';
import $ from 'jquery';

export default class Login extends React.Component {

	constructor(props) {
		super(props);

        this.handleChange = this.handleChange.bind(this)
        this.set_email = this.set_email.bind(this)

        this.state = {
            kindle: "",
            value: ""
        }
	}

    componentDidMount() {
        this.kindle()
    }

    handleChange(event)
    {
        this.setState(
            {
                value: event.target.value
            });
    }

    kindle() {
        $.ajax(
            {
                type: 'GET',
                url: '/kindle',
                dataType: 'json',
                success: function(data)
                {
                    this.setState(
                        {
                            kindle: data
                        });
                }.bind(this),
                error: function(xhr)
                {
                    console.log("error is " + xhr)
                }
            });
    }

    set_email() {
        var kindle = {
            email: this.state.value
        }

        $.ajax(
            {
                type: 'POST',
                url: '/set_email',
                data: kindle
            });

        this.setState(
            {
                kindle: this.state.value
            });

        
    }

	render () {
    return (
    	<div>
            <p>Your Kindle Email is {this.state.kindle}</p>
           <input value={this.state.value} onChange={this.handleChange} />
           <button onClick={this.set_email}>Set Email</button>
    	</div>
    	);
  }
}