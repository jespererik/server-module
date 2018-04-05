import React from 'react';
import { ListGroup, ListGroupItem, ButtonToolbar, Button} from 'react-bootstrap';
import './index.css';

export default class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = { reading: [] , nodes: [], locations: [], sensors: []};
  }

  componentDidMount() {
  }

  render() {
    // var listStyle = {
    //   // width:  500,
    //   // margin: 100,
    //   fontFamily: "monospace",
    //   fontSize: 12,
    //   backgroundColor: "#FFF",
    //   WebkitFilter: "drop-shadow(0px 0px 5px #666)",
    //   filter: "drop-shadow(0px 0px 5px #666)",
    //};
    return (
      <div >
        <Location  />
      </div>
    );
  }

}

class Location extends App {
  constructor(props){
    super(props)

    this.handleClick = this.handleClick.bind(this);

    this.state = {
      ...this.state,
      currentLocation: false
    }
  };

  handleClick(location) {
    this.setState({currentLocation: location});
  }

  componentDidMount() {
    this.fetchLocation();
  }

  fetchLocation(){
    fetch('http://localhost:3000/api/locations')
    .then(response => response.json())
    .then(jsonData =>{
      console.log(jsonData)
      const locations = jsonData.locations
      this.setState({locations})
    })
  }
  
  render() {
    const { currentLocation } = this.state;


    return (
      <div className="offset-md-4 col-md-4">
        <h4 align="center"> Locations </h4>
          <ListGroup>
            {this.state.locations.map((location, index) => 
            <div>
              <ListGroupItem key={index}> 
                <Button bsSize="large" block key={index} onClick={() => this.handleClick(location)}>
                  {location}
                </Button>
              </ListGroupItem>
              <ListGroupItem> {currentLocation === location ? <Nodes value = {location} /> : null } </ListGroupItem>
              </div>
            )}
          </ListGroup>  
      </div>);
  }

}


class Nodes extends App {
  constructor(props){
    super(props)
  };

  componentDidMount() {
    this.fetchNodes();
  }

  fetchNodes(){
    var location = this.props.value;
    var url = 'http://localhost:3000/api/locations/' + location + '/nodes';
    console.log(url);
    
    fetch(url)
    .then(response => response.json())
    .then(jsonData =>{
      console.log(jsonData)
      const nodes = jsonData.nodes.map(object => (object)) //this is an object with an array in it
      this.setState({nodes})
    })
  }

  render(){
    return( 
      <div className="offset-md-4 col-md-4">
        <ListGroup>
          {this.state.nodes.map((nodes, index) =>
            <ListGroupItem key={index}> {nodes.name} </ListGroupItem>
          )}
        </ListGroup>
    </div>);
  }

}

class Sensors extends App {
  constructor(props){
    super(props)
  };

  componentDidMount() {
    this.fetchSensors();
  }

  fetchSensors(){
    var location = 'inhouse';
    var node_name = 'NODE_4'
    var url = 'http://localhost:3000/api/locations/' + location + '/nodes' + '/' + node_name + '/sensors';
    console.log(url);
    
    fetch(url)
    .then(response => response.json())
    .then(jsonData =>{
      console.log(jsonData)
      const sensors = jsonData.sensors.map(object => (object)) //this is an object with an array in it
      this.setState({sensors})
    })
  }

  render(){
    return( 
      <div className="offset-md-4 col-md-4">
        <h4 align="center"> Sensors at NODE_4 </h4>
        <ListGroup>
          {this.state.sensors.map((sensors, index) =>
            <ListGroupItem key={index}> {sensors.name} </ListGroupItem>
          )}
        </ListGroup>
    </div>);
  }

}

class Readings extends App {
  constructor(props){
    super(props)
  };

  componentDidMount() {
    this.fetchReadings();
  }

  fetchReadings(){
    var location = 'inhouse';
    var node_name = 'NODE_4'
    var sensor_name = 'DHT11'
    var url = 'http://localhost:3000/api/locations/' + location + '/nodes' + '/' + node_name + '/sensors' + '/' + sensor_name + '/readings/latest';
    console.log(url);
    
    fetch(url)
    .then(response => response.json())
    .then(jsonData =>{
      console.log(jsonData)
      const reading = jsonData.reading.map(object => (object)) //this is an object with an array in it
      this.setState({reading})
    })
  }

  render(){
    return( 
      <div className="offset-md-4 col-md-4">
        <h4 align="center"> Latest reading for sensor DHT11 </h4>
        <ListGroup>
          {this.state.reading.map((reading, index) =>
            <ListGroupItem key={index}> Temp: {reading.data} Date: {reading.timestamp} </ListGroupItem>
          )}
        </ListGroup>
    </div>);
  }

}


