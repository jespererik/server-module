import React from 'react';
import { ListGroup, ListGroupItem, Button } from 'react-bootstrap';
import './index.css';

export default class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = { reading: [], nodes: [], locations: [], sensors: [] };
  }

  componentDidMount() {
  }

  render() {
      return (
      <div >
        <Location />
      </div>
    );
  }

}

class Location extends App {
  constructor(props) {
    super(props)

    this.handleClick = this.handleClick.bind(this);

    this.state = {
      ...this.state,
      currentLocation: false
    }
  };

  handleClick(location) {
    this.setState({ currentLocation: location });
  }

  componentDidMount() {
    this.fetchLocation();
  }

  fetchLocation() {
    var urlArr = window.location.href;
    urlArr = urlArr.split(':');
    console.log(urlArr);
    var url = urlArr[0] + ':' + urlArr[1] + ':3000/' + 'api/locations';
    console.log(url);

    // const username = prompt('Ange användarnamn');
    // const password = prompt('Ange lösen');

    fetch(url, {
      credentials: 'include',
    })
      .then(response => response.json())
      .then(jsonData => {
        console.log(jsonData)
        const locations = jsonData.locations
        this.setState({ locations })
      })
      .catch(err => {
        alert(err);
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
                <Button bsSize="large" bsStyle="primary" block key={index} onClick={() => this.handleClick(location)}>
                  {location}
                </Button>
              </ListGroupItem>
              <ListGroupItem> {currentLocation === location ? <Nodes location={location} /> : null} </ListGroupItem>
            </div>
          )}
        </ListGroup>
      </div>);
  }

}


class Nodes extends App {
  constructor(props) {
    super(props)

    this.handleClick = this.handleClick.bind(this);

    this.state = {
      ...this.state,
      currentNode: false
    }

  };

  handleClick(node) {
    this.setState({ currentNode: node.name });
  }

  componentDidMount() {
    this.fetchNodes();
  }

  fetchNodes() {
    var location = this.props.location;
    var urlArr = window.location.href;
    urlArr = urlArr.split(':');
    console.log(urlArr);
    var url = urlArr[0] + ':' + urlArr[1] + ':3000/' + 'api/locations' + '/' + location + '/nodes';
    console.log(url);

    fetch(url, {
      credentials: 'include',
    })
      .then(response => response.json())
      .then(jsonData => {
        console.log(jsonData)
        const nodes = jsonData.nodes
        this.setState({ nodes })
      })
  }

  render() {

    const { currentNode } = this.state;

    return (
      <div>
        <ListGroup>
          {this.state.nodes.map((node, index) =>
            <div>
              <ListGroupItem key={index}>
                <Button bsSize="large" bsStyle="info" block key={index} onClick={() => this.handleClick(node)}>
                  {node.name}
                </Button>
              </ListGroupItem>
              <ListGroupItem> {currentNode === node.name ? <Sensors nodeName={node.name} location={this.props.location} /> : null} </ListGroupItem>
            </div>
          )}
        </ListGroup>
      </div>);
  }

}

class Sensors extends App {
  constructor(props) {
    super(props)

    this.handleClick = this.handleClick.bind(this);

    this.state = {
      ...this.state,
      currentSensor: false
    }

  };

  handleClick(sensor) {
    this.setState({ currentSensor: sensor.name });
  }

  componentDidMount() {
    this.fetchSensors();
  }

  fetchSensors() {
    var location = this.props.location;
    var node_name = this.props.nodeName;
    var urlArr = window.location.href;
    urlArr = urlArr.split(':');
    console.log(urlArr);
    var url = urlArr[0] + ':' + urlArr[1] + ':3000/' + 'api/locations' + '/' + location + '/nodes' + '/' + node_name + '/sensors';
    console.log(url);

    fetch(url, {
      credentials: 'include',
    })
      .then(response => response.json())
      .then(jsonData => {
        console.log(jsonData)
        const sensors = jsonData.sensors
        this.setState({ sensors })
      })
  }

  render() {
    const { currentSensor } = this.state;

    return (
      <div>
        <ListGroup>
          {this.state.sensors.map((sensor, index) =>
            <div>
              <ListGroupItem key={index}>
                <Button bsSize="large" bsStyle="success" block key={index} onClick={() => this.handleClick(sensor)}>
                  {sensor.name}
                </Button>
              </ListGroupItem>
              <ListGroupItem> {currentSensor === sensor.name ? <Readings nodeName={this.props.nodeName} location={this.props.location} sensorName={sensor.name} /> : null} </ListGroupItem>
            </div>
          )}
        </ListGroup>
      </div>);
  }

}

class Readings extends App {
  constructor(props) {
    super(props)
  };

  componentDidMount() {
    this.fetchReadings();
  }

  fetchReadings() {
    var location = this.props.location;
    var node_name = this.props.nodeName;
    var sensor_name = this.props.sensorName;
    var urlArr = window.location.href;
    urlArr = urlArr.split(':');
    console.log(urlArr);
    var url = urlArr[0] + ':' + urlArr[1] + ':3000/' + 'api/locations' + '/' + location + '/nodes' + '/' + node_name + '/sensors' + '/' + sensor_name + '/readings/latest';
    console.log(url);

    fetch(url, {
      credentials: 'include',
    })
      .then(response => response.json())
      .then(jsonData => {
        console.log(jsonData)
        const reading = jsonData.reading 
        this.setState({ reading })
      })
  }

  render() {
    return (
      <div>
        <ListGroup>
          {this.state.reading.map((reading, index) =>
            <ListGroupItem key={index}> {reading.type} : {reading.data} Date: {reading.timestamp} </ListGroupItem>
          )}
        </ListGroup>
      </div>);
  }

}


