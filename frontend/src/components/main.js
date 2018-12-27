
import React, { Component } from 'react';
import '../App.css';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import ServersTable from './servers_table'
import RentTable from './rent_table'
import RentForm from './rent_form'
import DeleteRentForm from './delete_rent_form'
import api_url from '../const'
import ubuntu_logo from '../logo/ubuntu.png';
import fedora_logo from '../logo/fedora.png';
import centos_logo from '../logo/centos.png';
import '../../node_modules/react-bootstrap-table/css/react-bootstrap-table.css'
import "react-tabs/style/react-tabs.css";


// Main component of application
class MainComponent extends Component {
    
    constructor(props) {
        super(props);
        this.state = {
            servers: [],
            rents: [],
            server_id: '',
            rent_id: '',
            duration: '',
            user_id: 2
        }

        this.handleRentClick = this.handleRentClick.bind(this)
        this.handleDeleteClick = this.handleDeleteClick.bind(this)
    }


    handleChangeServerId = e => this.setState({server_id: e.target.value});
    handleChangeRentId = e => this.setState({rent_id: e.target.value});
    handleChangeDuration = e => this.setState({duration: e.target.value});

    validate_rent_input(server_id, duration) {
        return (server_id.length > 3)
    }

    async getServerInfo(server_id) {
        var response = await fetch('http://localhost:8080/server/' + server_id, {method: 'GET'});
        var body = await response.json();
        if (response.status === 200) {
            return body['server info']; 
        } else {
            console.log('Error: ' + body.message)
            return null;
        }
    }

    async getAllServers() {
        var response = await fetch('http://localhost:8080/server', {method: 'GET'});
        var body = await response.json();
        if (response.status === 200) {
            const servers = body.servers;
            var full_servers = [];
            for (var i = 0; i < servers.length; i++) {
                var server = await this.getServerInfo(servers[i].id);
                if (server) {
                    full_servers.push(server)
                }
            }
            
            return full_servers;
        } else {
            console.log('Error: ' + body.message)
            return null;
        }
    }

    async getUserRents(user_id) {
        var response = await fetch('http://localhost:8080/user/' + user_id + '/rent', {method: 'GET'});
        var body = await response.json();
        if (response.status === 200) {
            return body['user rents']; 
        } else {
            console.log('Error: ' + body.message)
            return null;
        }
    }

    handleDeleteClick() {
        
        if (this.validate_rent_input(this.state.rent_id)) {
            alert('OK')
        } else {
          alert(this.state.rent_id)
        }
    }

    handleRentClick() {
        //var new_servers = this.state.servers.slice();
        //new_servers[0].name = Math.random().toString(36).substring(7);;
        //new_servers[1].name = this.state.value
     
        if (this.validate_rent_input(this.state.server_id)) {
            alert('OK')
        } else {
          alert(this.state.server_id)
        }
        
        // checkValid
        // Post request
        // Get request to update info
        // setState 

        //this.setState({
        //  servers: new_servers});
      }
    
    async componentWillMount() {

        var all_servers = await this.getAllServers();
        //console.log(all_servers)
        if (all_servers) {
            this.setState({
                servers: all_servers
            });
        } else {
            alert("Error: can not get info about servers. Try later.")
        }
        
        var user_rents = await this.getUserRents(this.state.user_id);
        if (user_rents !== null) {
            this.setState({
                rents: user_rents
            });
        } else {
            alert("Error: can not get about your rents. Try later.")
        }

       
        // request to get all user_rents
        // request to gateway for initializing servers and rent
    }

    render() {
        return(
            <div>
                <div className="Header" >
                    <h1>Web Hosting Service</h1>
                    <div>
                        <img src={ubuntu_logo} className="Logo"/>
                        <img src={fedora_logo} className="Logo"/>
                        <img src={centos_logo} className="Logo"/>
                    </div>
                </div>
                <div>
                    <Tabs className="Header">
                        <TabList>
                            <Tab>Rent server</Tab>
                            <Tab>Your rents</Tab>
                        </TabList>
                        <TabPanel>
                            <h2>Available servers</h2>
                            <div>
                                <ServersTable data={this.state.servers}/>
                                <RentForm handleClick={this.handleRentClick}
                                            server_id={this.state.server_id}
                                            duration={this.state.duration}
                                            onChangeDuration={this.handleChangeDuration}
                                            onChangeServerId={this.handleChangeServerId}/>
                            </div>
                        </TabPanel>
                        <TabPanel>
                            <RentTable data={this.state.rents}/>
                            <DeleteRentForm handleClick={this.handleDeleteClick}
                                            rent_id={this.state.rent_id}
                                            onChangeRentId={this.handleChangeRentId}/>
                        </TabPanel>
                    </Tabs>
                </div>

            </div>
        );
    }
}

export default MainComponent;