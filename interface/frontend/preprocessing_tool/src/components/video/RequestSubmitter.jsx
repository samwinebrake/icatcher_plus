import { 
  TextField, 
  Button
} from '@mui/material';
import { useState, Fragment, useCallback, useEffect, } from 'react';
import {io} from 'socket.io-client'


function Login() {
  const [username, setUser] = useState("")
  const [password, setPassword] = useState("")
  const [path, setPath] = useState("")
  const [ic, setIC] = useState("")
  const [global_data, setData] = useState("");
  const [socketInstance, setSocketInstance] = useState("")
  const [buttonState, setButtonState] = useState(false)
  const [userError, setUserError] = useState(false)
  const [passwordError, setPasswordError] = useState(false)
  const [pathError, setPathError] = useState(false)
  const [icError, setICError] = useState(false)


  const handleSubmit = (event) => {
      event.preventDefault();

      if (username && password) {
        console.log(username, password);
        setButtonState(true)
      }
      else {
        setButtonState(false)
      }
  };

  useEffect(() => {
    if (buttonState === true) {
      var ssh_info = {
        "host": "@openmind7.mit.edu",
        "username": username,
        "password": password
      };
        const socket = io("localhost:5001/", {
          transports: ["websocket"],
          // cors: {
          //   origin : "localhost:3000",
          // },
        });
        socket.on("connect", (data) => {
          console.log(data);

          // fetch("localhost:3000/http-call", {
          //   headers: {
          //     "Content-Type": "application/json",
          //   },
          // })
          //   .then(response => response.json())
          //   .then((responseData) => {
          //     setData(responseData.data);
          //   });

            console.log(global_data)
            // socket.emit("data", data)
        });
  
        socket.on("disconnect", (data) => {
          console.log(data);
          setButtonState(false)
        });


      return function cleanup() {
        socket.disconnect();
      };
    }
  }, [buttonState]);
   
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
                  label="Path to iCatcher+ install"
                  onChange={e => setIC(e.target.value)}
                  required
                  variant="outlined"
                  color="secondary"
                  type="text"
                  value={ic}
                  error={icError}
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