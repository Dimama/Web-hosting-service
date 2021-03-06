import React, { Component } from 'react';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';


class RentTable extends Component {
    render() {
        return(
            <BootstrapTable className="Table" data={ this.props.data }>
                <TableHeaderColumn width="7%" className="Header" dataField='id' isKey={ true }>ID</TableHeaderColumn>
                <TableHeaderColumn width="30%" className="Header" dataField='OS'>OS</TableHeaderColumn>
                <TableHeaderColumn width="8%" className="Header" dataField='CPU'>CPU</TableHeaderColumn>
                <TableHeaderColumn className="Header" dataField='RAM'>RAM,Gb</TableHeaderColumn>
                <TableHeaderColumn className="Header" dataField='Drive'>Drive,Gb</TableHeaderColumn>
                <TableHeaderColumn className="Header" dataField='price'>Price,$</TableHeaderColumn>
                <TableHeaderColumn className="Header" dataField='duration'>Duration</TableHeaderColumn>
            </BootstrapTable>
        );
    }
}

export default RentTable;