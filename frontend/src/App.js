import React from 'react';
import { ListGroup, ListGroupItem} from 'react-bootstrap';
import './index.css';

export default class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = { readings: [] , nodes: []};
  }

  componentDidMount() {
    this.fetchReadings();
    this.fetchNodes();
  }

  fetchReadings(){
    fetch('http://localhost:3000/api/nodes/NODE_1/sensors/DHT11/readings')
    .then(response => response.json())
    .then(jsonData =>{
      console.log(jsonData)
      const readings = jsonData.map(object => (object));
      this.setState({readings})
    })
  }

  fetchNodes(){
    fetch('http://localhost:3000/api/nodes')
    .then(response => response.json())
    .then(jsonData =>{
      console.log(jsonData)
      const nodes = jsonData.nodes.map(object => (object)) //this is an object with an array in it
      this.setState({nodes})
    })
  }

  render() {
    var listStyle = {
      // width:  500,
      // margin: 100,
      fontFamily: "monospace",
      fontSize: 12,
      backgroundColor: "#FFF",
      WebkitFilter: "drop-shadow(0px 0px 5px #666)",
      filter: "drop-shadow(0px 0px 5px #666)",
    };
    return (
      <div style={listStyle} className="offset-md-4 col-md-4">
        <h4 align="center"> Nodes </h4>
        <ListGroup>
          {this.state.nodes.map((nodes, index) =>
            <ListGroupItem key={index}> Name: {nodes.name} Location: {nodes.location} Created: {nodes.created}  </ListGroupItem>
          )}
        </ListGroup>
      </div>
    );
  }

}


