import React, { useEffect } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/user/1', {
      method: "GET",
      mode: "cors"
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data)
      })
      .catch(error => {
        console.error(error)
      })
  }, []);


  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;