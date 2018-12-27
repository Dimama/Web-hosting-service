import React, { Component } from 'react';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';


class RentTable extends Component {
    
    constructor(props) {
        super(props);
    }
    
    render() {

        return(
            <BootstrapTable data={ this.props.data }>
                <TableHeaderColumn dataField='id' isKey={ true }>ID</TableHeaderColumn>
                <TableHeaderColumn dataField='OS'>OS</TableHeaderColumn>
                <TableHeaderColumn dataField='CPU'>CPU</TableHeaderColumn>
                <TableHeaderColumn dataField='RAM'>RAM,Gb</TableHeaderColumn>
                <TableHeaderColumn dataField='Drive'>Drive,Gb</TableHeaderColumn>
                <TableHeaderColumn dataField='price'>Price,$</TableHeaderColumn>
                <TableHeaderColumn dataField='duration'>Duration</TableHeaderColumn>
            </BootstrapTable>
        );
    }
}

export default RentTable;