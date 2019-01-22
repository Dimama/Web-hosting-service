import React from 'react';


class Oauth2Form extends React.Component {
    render() {
        return (
            <div>
                <div><h3>
                        Input login and password and press 'OK' to allow application access to your data 
                    </h3>
                </div>
                <div>
                    <input className="Input" type="text" name="login" placeholder="login"
                        value={this.props.login} onChange={this.props.onChangeLogin}/>
                </div>
                <div>
                    <input className="Input" type="text" name="password" placeholder="password"
                            value={this.props.password} onChange={this.props.onChangePassword}/>
                </div>
                <div>
                    <button className="Button" onClick={this.props.handleLogInClick}>
                        OK
                    </button>
                </div>
          </div>
      );
    }
  }

export default Oauth2Form;