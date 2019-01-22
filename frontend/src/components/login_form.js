import React from 'react';


class LoginForm extends React.Component {
    render() {
        return (
            <div>
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
                        Login
                    </button>
                </div>
                <div>
                    {this.props.button}
                </div>
          </div>
      );
    }
  }

export default LoginForm;