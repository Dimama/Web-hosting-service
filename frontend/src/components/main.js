
import React, { Component } from 'react';
import '../App.css';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';

import ServersTable from './servers_table'
import RentTable from './rent_table'
import RentForm from './rent_form'
import DeleteRentForm from './delete_rent_form'
import LoginForm from './login_form'

import API_URL from '../const'

import jwt_decode from '../../node_modules/jwt-decode'

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
            isLoggedIn: false,
            login: '',
            password: ''
        }
        
        localStorage.setItem('access_token', '');
        localStorage.setItem('refresh_token', '');

        this.handleRentClick = this.handleRentClick.bind(this)
        this.handleDeleteClick = this.handleDeleteClick.bind(this)
        this.handleLoginClick = this.handleLoginClick.bind(this)
        this.handleLogoutClick = this.handleLogoutClick.bind(this)
    }


    handleChangeServerId = e => this.setState({server_id: e.target.value});
    handleChangeRentId = e => this.setState({rent_id: e.target.value});
    handleChangeDuration = e => this.setState({duration: e.target.value});
    handleChangeLogin = e => this.setState({login: e.target.value});
    handleChangePassword = e => this.setState({password: e.target.value});

    validate_rent_input(server_id, duration) {
        return ((server_id.match(/^\d+$/))
                && (duration.match(/^\d+$/))
                && (parseInt(duration) !== 0)
                && (parseInt(server_id) !== 0))
    }

    validate_delete_input(rent_id) {
        return ((rent_id.match(/^\d+$/)) && (parseInt(rent_id) !== 0))
    }

    get_user_id(){
        return jwt_decode(localStorage.getItem('access_token'))['sub']
    }

    async handleLoginClick() {
        var request_data = {
            method: 'POST',
            body: JSON.stringify({
                login: this.state.login,
                password: this.state.password}),
            headers: { 'Content-Type': 'application/json' }
        }

        var response = await fetch(API_URL + 'login', request_data);
        var body = await response.json();

        if (response.status === 200) {
            localStorage.setItem('access_token', body.access_token)
            localStorage.setItem('refresh_token', body.refresh_token)
            this.setState({isLoggedIn: true});
            await this.updateUserRents();
        } else {
            alert('Error: ' +  body.message);
        }
    }

    async handleLogoutClick(){
        localStorage.setItem('access_token', '') // remove item?
        localStorage.setItem('refresh_token', '')
        this.setState({isLoggedIn: false});
    }

    async refresh() {
        var request_data = {
            method: 'POST',
            body: JSON.stringify({refresh_token: localStorage.getItem('refresh_token'),}),
            headers: { 'Content-Type': 'application/json' }
        }

        var response = await fetch(API_URL + 'refresh', request_data);
        var body = await response.json();
        if (response.status === 200) {
            localStorage.setItem('access_token', body.access_token)
        } else {
            alert('Server Error. You need to relogin');
        }

    }

    async getServerInfo(server_id) {
        var response = await fetch(API_URL + 'server/' + server_id, {method: 'GET'});
        var body = await response.json();
        if (response.status === 200) {
            return body['server info']; 
        } else {
            console.log('Error: ' + body.message)
            return null;
        }
    }

    async getAllServers() {
        var response = await fetch(API_URL + 'server', {method: 'GET'});
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

    async getUserRents() {

        var user_id = this.get_user_id();
        var request_data = {
            method: 'GET',
            headers: { 'Authorization':
             'Bearer ' + localStorage.getItem('access_token')}
        }
        var response = await fetch(API_URL + 'user/' + user_id + '/rent', request_data);
        var body = await response.json();

        if(response.status === 401) {
            this.refresh();
            console.log("Token expired")
            await this.getUserRents();
        } else if (response.status === 200) {
            return body['user rents']; 
        } else {
            console.log('Error: ' + body.message)
            return null;
        }
    }

    async handleDeleteClick() {
        if (this.validate_delete_input(this.state.rent_id)) {

            var user_id = this.get_user_id();
            var request_data = {
                method: 'DELETE',
                headers: { 'Authorization':
                 'Bearer ' + localStorage.getItem('access_token')}
            }
            var response = await fetch(API_URL + 'user/' + user_id +
                                     '/rent/' + this.state.rent_id, request_data);

            if(response.status === 401) {
                this.refresh();
                alert("Error during request. Repeat please.")
            } else if (response.status === 400) {
                alert("Error: bad request");
            } else if (response.status === 404) {
                var body = await response.json()
                alert("Error: " +  body.message);
            } else { // deleted
                alert("Rent was deleted")
                await this.updateUserRents();
                await this.updateServers();
            }
        } else {
            alert("Error: rent id must be positive integer");
        }
    }

    async handleRentClick() {
        if (this.validate_rent_input(this.state.server_id, this.state.duration)) {

            var request_data = {
                method: 'POST',
                body: JSON.stringify({
                    duration: this.state.duration,
                    server_id: this.state.server_id}),
                headers: { 'Content-Type': 'application/json',
                            'Authorization':
                            'Bearer ' + localStorage.getItem('access_token') }
            }
            
            var user_id = this.get_user_id();
            var response = await fetch(API_URL + 'user/' + user_id + '/rent',
                 request_data);
            var body = await response.json()

            if(response.status === 401) {
                this.refresh();
                alert("Error during request. Repeat please.")
            } else if (response.status === 400) {
                alert("Error: bad request");
            } else if (response.status === 404) {
                alert("Error: " + body.message);
            } else if (response.status === 422) {
                alert("Warning: " + body.message);
            } else if (response.status >= 500) {
                alert("Server Error: " + body.message)
            } else { // created
                alert("Successfull rent!")
                await this.updateUserRents();
                await this.updateServers();
            }

        } else {
          alert("Error: duration and id must be positive integer");
        }
        
      }
    
    async updateUserRents() {
        var user_rents = await this.getUserRents();
        if (user_rents !== []) {
            this.setState({
                rents: user_rents
            });
        } else {
            alert("Error: can not get info about your rents. Try later.")
        }
    }

    async updateServers() {
        var all_servers = await this.getAllServers();
        if (all_servers) {
            this.setState({
                servers: all_servers
            });
        } else {
            alert("Error: can not get info about servers. Try later.")
        }
    }

    async componentWillMount() {
        await this.updateServers();
    }

    render() {
        const isLoggedIn = this.state.isLoggedIn;

        return(
            <div className="App">
                <div className="left">
                    {isLoggedIn &&
                        <button className="Button" onClick={this.handleLogoutClick}>
                            Logout
                        </button>
                    }
                    {!(isLoggedIn) &&
                        <div>
                            <LoginForm  isLoggedIn={isLoggedIn}
                                        login={this.state.login}
                                        password={this.state.password}
                                        handleLogInClick={this.handleLoginClick}
                                        onChangeLogin={this.handleChangeLogin}
                                        onChangePassword={this.handleChangePassword}
                            />
                        </div>
                    }

                </div>

                <div className="Basic">
                    <h1 className="Header">Web Hosting Service</h1>
                    <div>
                        <img src={ubuntu_logo} className="Logo"/>
                        <img src={fedora_logo} className="Logo"/>
                        <img src={centos_logo} className="Logo"/>
                    </div>

                    <Tabs>
                        <TabList className="Tabs">
                            <Tab>Rent server</Tab>
                            {isLoggedIn &&
                                <Tab>Your rents</Tab>
                            }
                        </TabList>
                        <TabPanel>
                            <h2  className="Header">Available servers</h2>
                            <div>
                                <ServersTable data={this.state.servers}/>
                                {isLoggedIn &&
                                    <RentForm handleClick={this.handleRentClick}
                                                server_id={this.state.server_id}
                                                duration={this.state.duration}
                                                onChangeDuration={this.handleChangeDuration}
                                                onChangeServerId={this.handleChangeServerId}/>
                                }
                            </div>
                        </TabPanel>
                            {isLoggedIn &&
                                <TabPanel className="Tab">
                                    <RentTable className="Table" data={this.state.rents}/>
                                    <DeleteRentForm handleClick={this.handleDeleteClick}
                                            rent_id={this.state.rent_id}
                                            onChangeRentId={this.handleChangeRentId}/>
                                </TabPanel>
                            }    
                    </Tabs>
                </div>
            </div>
        );
    }
}

export default MainComponent;