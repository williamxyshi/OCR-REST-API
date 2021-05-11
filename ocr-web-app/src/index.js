import {useState, useEffect} from 'react';
import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import reportWebVitals from './reportWebVitals';
import { Route, BrowserRouter as Router, Switch, Redirect } from 'react-router-dom';
import LandingPage from './components/LandingPage'
import SignInPage from './components/SignInPage'
import axios from 'axios'
import SignUpPage from './components/SignUpPage';
import Dashboard from './components/Dashboard';

function App(props) {
  const [jwt, setJwt] = useState('no key');
  const [user, setUser] = useState({
    email: "",
    calls: -1,
    key: ""
  });

  useEffect(() => {
    let token = localStorage.getItem('token')
    setJwt(token)
    axios.defaults.headers.common['token'] = token;
  });
  
  const ProtectedRoute = ({ component: Component, user, ...rest }) => {
    console.log(user)
    return (
      <Route {...rest} render={
        props => {
          if (user) {
            return <Component user={user} {...rest} {...props} />
          } else {
            return <Redirect to={
              {
                pathname: '/',
              }
            } />
          }
        }
      } />
    )
  }
  const setJwtToken = (token) => {
    axios.defaults.headers.common['token'] = token;
    setJwt(token)
    localStorage.setItem('token', token);
  }
  const setUserModel = (user) => {
    setUser(user)
    console.log(user)
  }


  return (
    <React.StrictMode>
      <Router>
        <Switch>
            <Route path = "/signin" component={()=> <SignInPage setJwtToken={setJwtToken} setUserModel={setUserModel}/>} />
            <Route path = "/signup" component={()=> <SignUpPage />} />
            <ProtectedRoute exact path='/dashboard' user={user} jwt={jwt} setUserModel={setUserModel} component={Dashboard} />
            <Route path='/contact' component={() => { 
                window.location.href = 'https://teahouseapps.app/#contact'; 
                return null;
            }}/>
            <Route path = "/" component={LandingPage} />
        </Switch>

      </Router>
    </React.StrictMode>
  )
}

ReactDOM.render(
  <App/>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
