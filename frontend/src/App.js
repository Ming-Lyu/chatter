import logo from './logo.svg';
import './App.css';  
import React from 'react';
import ReactDOM from 'react-dom';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <MyComponent />
      </header>
    </div>
  );
}

class MyComponent extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            data:[],
            loaded: false,
        };
    }

    componentDidMount() {
      const apiUrl = 'http://localhost:8000/chatter_api/';
      fetch(apiUrl)
      .then(response => {
        if (response.status > 400) {
          return this.setState(() => {
            return { placeholder: "Something went wrong!" };
          });
        }
        return response.json();
      })
      .then(data => {
        this.setState(() => {
          console.log(data)
          return {
            data,
            loaded: true
          };
        });
      });
    }
        // .then((data) => console.log('This is your data', data));
      
    render(){
    //   return <h1>this is ? `${this.state}`</h1>;
        return <h1>test</h1>
    }
}

export default App;
