import React from 'react';
import ReactDOM from 'react-dom';
import { ListGroup, ListGroupItem, Panel } from 'react-bootstrap';
import './index.css';

export default class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = { readings: [] };
  }

  componentDidMount() {
    fetch('http://localhost:5000/api/nodes/NODE_1/sensors/DHT11/readings')
    .then(response => response.json())
    .then(json =>{
      console.log(json)
      const readings = json.map(object => (object));
      this.setState({readings})
    })
}

  render() {
    var listStyle = {
      width:  500,
      margin: 100,
      fontFamily: "monospace",
      fontSize: 12,
      backgroundColor: "#FFF",
      WebkitFilter: "drop-shadow(0px 0px 5px #666)",
      filter: "drop-shadow(0px 0px 5px #666)",
    };
    return (
      <div style={listStyle}>
        <h4 align="center"> Readings </h4>
        <ListGroup>
          {this.state.readings.map((reading, index) =>
            <ListGroupItem key={index}> Date: {reading.timestamp} : Temperature {reading.data} C</ListGroupItem>
          )}
        </ListGroup>
      </div>
    );
  }

}


