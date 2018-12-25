import React, { Component } from 'react';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';


class ServersTable extends Component {
    
    constructor(props) {
        super(props);
    }
    
    render() {

        const paginate_options = {
            page: 1,  // which page you want to show as default
            sizePerPageList: [], // you can change the dropdown list for size per page
            sizePerPage: 3,  // which size per page you want to locate as default
            pageStartIndex: 1, // where to start counting the pages
            paginationSize: 3,  // the pagination bar size.
            prePage: 'Prev', // Previous page button text
            nextPage: 'Next', // Next page button text
            firstPage: 'First', // First page button text
            lastPage: 'Last', // Last page button text
            paginationShowsTotal: this.renderShowsTotal,  // Accept bool or function
            paginationPosition: 'bottom'  // default is bottom, top and both is all available
            // keepSizePerPageState: true //default is false, enable will keep sizePerPage dropdown state(open/clode) when external rerender happened
            // hideSizePerPage: true > You can hide the dropdown for sizePerPage
            // alwaysShowAllBtns: true // Always show next and previous button
            // withFirstAndLast: false > Hide the going to First and Last page button
            // hidePageListOnlyOnePage: true > Hide the page list if only one page.
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