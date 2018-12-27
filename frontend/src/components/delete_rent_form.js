import React, { Component } from 'react';


class DeleteRentForm extends React.Component {
    render() {
      return (
          <div>
            <input className="Input" type="text" name="rent id" placeholder="rent id"
                    value={this.props.rent_id} onChange={this.props.onChangeRentId}/>
            <button className="Button" onClick={this.props.handleClick}>
              Delete rent
            </button>
          </div>
      );
    }
  }

export default DeleteRentForm;