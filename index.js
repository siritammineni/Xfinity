import React from 'react';
import {createRoot} from 'react-dom/client';
//import './index.css';
import App from './App';
//import reportWebVitals from './reportWebVitals';
import { GoogleOAuthProvider } from '@react-oauth/google';

const container = document.getElementById('root')


const root = createRoot(container);
root.render(
    <GoogleOAuthProvider clientId='148948074621-e195j5k6q515avhsehau1b44m13kc75g.apps.googleusercontent.com'>
        <App />
    </GoogleOAuthProvider>
);
//---------------//
// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
//---------------//
//reportWebVitals();

