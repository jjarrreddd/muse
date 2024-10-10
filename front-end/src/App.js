// In order to launch full web app, split terminal and run FLASK
// in one terminal and REACT in the other terminal.
// To run: npm start, while in 'front-end' directory

import { useState } from 'react'
import axios from "axios"
import './App.css'

function App() {

  const [profileData, setProfileData] = useState(null) // contol the state of 'profileData'

  function getData() {
    axios({
      method: "GET",
      url:"/welcome",
    })
    .then((response) => {
      const res =response.data
      setProfileData(({
        profile_name: res.name,
        profile_hello: res.hello}))
    }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        console.log(error.response.status)
        console.log(error.response.headers)
        }
    })}
    //end of new line 

  return (
    <div className="App">
      <header className="App-header" style={{ backgroundColor: 'black', color: 'white'}}>  // Background color change, green to black
        <h1 style={{fontSize: '4rem'}}>Muse</h1>  // Muse text
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>

        {/* new line start*/}
        <p>To get your profile details: </p><button onClick={getData}>Click me</button>
        {profileData && <div>
              <p>Greeting (front end): {profileData.profile_name}</p>
              <p>About me (front end): {profileData.profile_hello}</p>
            </div>
        }
         {/* end of new line */}
      </header>
    </div>
  );
}

export default App;
