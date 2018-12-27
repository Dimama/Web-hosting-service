import React, { Component } from 'react';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';


class ServersTable extends Component {  
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
            <BootstrapTable className="Table" data={ this.props.data } pagination={ true } options={ paginate_options }>
                <TableHeaderColumn className="Header" dataField='id' isKey={ true }>ID</TableHeaderColumn>
                <TableHeaderColumn className="Header" dataField='OS'>OS</TableHeaderColumn>
                <TableHeaderColumn className="Header" dataField='CPU'>CPU</TableHeaderColumn>
                <TableHeaderColumn className="Header" dataField='Drive'>Drive,Gb</TableHeaderColumn>
                <TableHeaderColumn className="Header" dataField='RAM'>RAM,Gb</TableHeaderColumn>
                <TableHeaderColumn className="Header" dataField='price'>Price,$</TableHeaderColumn>
                <TableHeaderColumn className="Header" dataField='count'>Count</TableHeaderColumn>
            </BootstrapTable>
        );
    }
}

export default ServersTable;