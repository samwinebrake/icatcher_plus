import { 
  TextField, 
  Button
} from '@mui/material';
import { useState, Fragment } from 'react';
import {io} from 'socket.io-client'
import {allow} from 'allow-cors'
import useWebSocket, { ReadyState } from 'react-use-websocket';


/* Expected props:
  tbd
  */
 
const socketUrl = 'ws://localhost:60371';



const HOST = "localhost"
const PORT = 60371

function connect() {
  return new Promise(function(resolve, reject) {
      var server = new WebSocket('ws://'+HOST+':'+PORT);
      server.onopen = function() {
          resolve(server);
      };
      server.onerror = function(err) {
          reject(err);
      };

  });
}


function Login() {
  const [username, setUser] = useState("")
  const [password, setPassword] = useState("")
  const [path, setPath] = useState("")
  const [userError, setUserError] = useState(false)
  const [passwordError, setPasswordError] = useState(false)
  const [pathError, setPathError] = useState(false)
  const socket = new WebSocket('ws://localhost:60371', "json");
  // const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl);
  var ssh_info = {"data" : {
    "host": "@openmind7.mit.edu",
    "username": username,
    "password": password
  }};
  
  
  // const [] = useState()

  const handleSubmit = (event) => {
      event.preventDefault();

      setUserError(false);
      setPasswordError(false);

      if (username === '') {
          setUserError(true);
      };
      if (password === '') {
          setPasswordError(true);
      };
      if (path === '') {
        setPathError(true);
    };

      if (username && password) {
        // console.log(username, password);
        // connect().then(function(server) {
        //   // server is ready here
        // sendMessage(ssh_info)
        var msg = {
              ws_op : "send",
              ws_msg : "49.138077,-122.857472"
          };
          socket.send( JSON.stringify("msg") );
          // msg_div.innerHTML += "<p>Message is sent...</p>";
          // msg_div.innerHTML += "<p>Waiting for response...</p>";
        }
      // }).catch(function(err) {
      //     // error here
      // });

  };
   
  return ( 
      <Fragment>
      <form autoComplete="off" onSubmit={handleSubmit}>
          <h2>iCatcher+ Remote Tool</h2>
              <TextField 
                  label="Username"
                  onChange={e => setUser(e.target.value)}
                  required
                  variant="outlined"
                  color="secondary"
                  type="text"
                  sx={{mb: 3}}
                  fullWidth
                  value={username}
                  error={userError}
               />
               <TextField 
                  label="Password"
                  onChange={e => setPassword(e.target.value)}
                  required
                  variant="outlined"
                  color="secondary"
                  type="password"
                  value={password}
                  error={passwordError}
                  fullWidth
                  sx={{mb: 3}}
               />
               <TextField 
                  label="Path to data"
                  onChange={e => setPath(e.target.value)}
                  required
                  variant="outlined"
                  color="secondary"
                  type="text"
                  value={path}
                  error={pathError}
                  fullWidth
                  sx={{mb: 3}}
               />
               <Button variant="outlined" color="secondary" type="submit">Login</Button>
           
      </form>
      <small>Note: Must be able to submit batch jobs to OpenMind to use remote version of iCatcher+.</small>
      </Fragment>
   );
}

export default Login;