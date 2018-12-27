import React, { Component } from 'react';


class RentForm extends React.Component {
    render() {
      return (
          <div>
            <input type="text" name="duration" placeholder="duration"
                   value={this.props.duration} onChange={this.props.onChangeDuration}/>
            <input type="text" name="server id" placeholder="server id"
                    value={this.props.server_id} onChange={this.props.onChangeServerId}/>
            <button onClick={this.props.handleClick}>
              Rent server
            </button>
          </div>
      );
    }
  }

export default RentForm;