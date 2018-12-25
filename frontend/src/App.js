import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import { TableSimple } from 'react-pagination-table';
import api_url from './const.js'

const PLACES = [
  { name: "Palo Alto", zip: "94303" },
  { name: "San Jose", zip: "94088" },
  { name: "Santa Cruz", zip: "95062" },
  { name: "Honolulu", zip: "96803" }
];

class App extends Component {
  render() {
    return (
      <div className="App">
        <ServersTable/>
        <WeatherDisplay zip={"12345"}/>
        {PLACES.map((place, index) => (
          <button
            key={index}
          >
            {place.name}
          </button>
        ))}
        <div className="App-header">
          <img src={logo} className="App-logo"/>
          <h2>Welcome to React</h2>
          <p className="App-intro">
            To get started edit <code>src/App.js</code> and save it to reload
          </p>
        </div>
      </div>

    );
  }
}

class WeatherDisplay extends Component {
  render() {
    return (
      <h1>Displaying weather for city {this.props.zip}</h1>
      
    );
  }
}

const data = [
  { size: ["L", "M"], phone: 1234567, gender: "Male", age: 20, name:"Ben" },
  { size: ["L", "M", "XL"], phone: 1234567, gender: "Female", age: 22, name:"Ken" },
  { size: ["L", "S"], phone: 1234567, gender: "Female", age: 23, name:"Jay" },
  { size: ["M", "S"], phone: 1234567, gender: "Male", age: 26, name:"Chip" },
  { size: ["XL", "XS"], phone: 1234567, gender: "Male", age: 23, name:"Lee" },
  { size: ["L", "M", "S", "XS"], phone: 1234567, gender: "Female", age: 30, name:"Frank" },
  { size: ["S", "L"], phone: 1234567, gender: "Male", age: 23, name:"CoCo" },
  { size: ["L", "M", "S"], phone: 1234567, gender: "Female", age: 20, name:"Fake" },
  { size: ["XS", "L"], phone: 1234567, gender: "Male", age: 26, name:"Dump" },
  { size: ["L", "M", "S"], phone: 1234567, gender: "Female", age: 27, name:"Ocean" },
  { size: ["S", "XL"], phone: 1234567, gender: "Male", age: 20, name:"Polo" },
  { size: ["M", "XL"], phone: 1234567, gender: "Female", age: 21, name:"Queen" },
  { size: ["L", "M"], phone: 1234567, gender: "Female", age: 20, name:"Bump" },
  { size: ["L", "M", "S", "XL"], phone: 1234567, gender: "Male", age: 22, name:"Judy" },
  { size: ["XL", "M"], phone: 1234567, gender: "Female", age: 24, name:"Ryan" },
  { size: ["L", "S"], phone: 1234567, gender: "Female", age: 25, name:"Flow" },
  { size: ["S", "M"], phone: 1234567, gender: "Female", age: 31, name:"Ray" },
  { size: ["L", "M", "XS"], phone: 1234567, gender: "Male", age: 23, name:"Yen" },
  { size: ["XL", "M", "S"], phone: 1234567, gender: "Male", age: 21, name:"Gray" },
  { size: ["L", "M", "S"], phone: 1234567, gender: "Female", age: 22, name:"Tom" }
];

class ServersTable extends Component {
  
  constructor(props) {
    super(props);
    this.Header = ["Name", "Age", "Size", "Phone", "Gender" ];
  }

  render() {
    return (
      <div className="ServersTable">
        <TableSimple
        title="TableSimple"
        subTitle="Sub Title"
        headers={ this.Header }
        data={ data }
        columns="name.age.size.phone.gender"
        arrayOption={ [["size", 'all', ', ']] }
        />
        <h2>api_url</h2>
      </div>
    );
  }
}
export default App;
