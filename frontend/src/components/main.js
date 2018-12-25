
import React, { Component } from 'react';
import '../App.css';
import ServersTable from './servers_table'
import api_url from '../const'
import ubuntu_logo from '../logo/ubuntu.png';
import fedora_logo from '../logo/fedora.png';
import centos_logo from '../logo/centos.png';


// Main component of application
class MainComponent extends Component {
    
    constructor(props) {
        super(props);
        this.state = {
            servers: [],
            rent: [],
        }
    }

    componentWillMount() {
        const n_servers = [
            {'CPU': 6,
             'Drive': 320,
             'OS': 'Ubuntu 16.04 Server',
             'RAM': 16,
             'count': 20,
             'id': 1,
             'price': 80,
        },]

        this.setState({
            servers: n_servers
        })
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
            <div className="Servers-Table">
                <ServersTable data={this.state.servers}/>
            </div>
            </div>
        );
    }
}

export default MainComponent;