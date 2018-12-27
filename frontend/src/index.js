import React from 'react';
import ReactDOM from 'react-dom';
import MainComponent from './components/main.js'
import * as serviceWorker from './serviceWorker';
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';

ReactDOM.render(<MainComponent/>, document.getElementById('root'));

serviceWorker.unregister();
