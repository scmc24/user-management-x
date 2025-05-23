import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import {BrowserRouter} from "react-router-dom";
import axios  from 'axios';
import {Provider} from 'react-redux'

import { store } from './store';

axios.defaults.baseURL = "http://127.0.0.1:8079/ACCOUNT-SERVICE/api";
//axios.defaults.baseURL = "http://0.0.0.0:8083/api";

let token = window.localStorage.getItem("token");
if(token) axios.defaults.headers.common["Authorization"] = `Token ${token}`; 

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
    <Provider store={store} >
       <App  />
    </Provider>
   
    </BrowserRouter>
    
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
