import React, { Component } from 'react';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';


class ServersTable extends Component {
    
    constructor(props) {
        super(props);
    }
    
    render() {

        const paginate_options = {
            page: 1,
            sizePerPageList: [],
            sizePerPage: 3,
            pageStartIndex: 1,
            paginationSize: 3,
            prePage: 'Prev',
            nextPage: 'Next',
            firstPage: 'First',
            lastPage: 'Last',
            paginationShowsTotal: this.renderShowsTotal,
            paginationPosition: 'bottom'

          };
        return(
            <BootstrapTable data={ this.props.data } pagination={ true } options={ paginate_options }>
                <TableHeaderColumn dataField='id' isKey={ true }>ID</TableHeaderColumn>
                <TableHeaderColumn dataField='OS'>OS</TableHeaderColumn>
                <TableHeaderColumn dataField='CPU'>CPU</TableHeaderColumn>
                <TableHeaderColumn dataField='Drive'>Drive,Gb</TableHeaderColumn>
                <TableHeaderColumn dataField='RAM'>RAM,Gb</TableHeaderColumn>
                <TableHeaderColumn dataField='price'>Price,$</TableHeaderColumn>
                <TableHeaderColumn dataField='count'>Count</TableHeaderColumn>
            </BootstrapTable>
        );
    }
}

export default ServersTable;