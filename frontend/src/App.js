import React from 'react';
import { ListGroup, ListGroupItem} from 'react-bootstrap';
import './index.css';

export default class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = { readings: [] , nodes: [], locations: []};
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
  };

  componentDidMount() {
    this.fetchLocation();
  }

  fetchLocation(){
    fetch('http://localhost:3000/api/locations')
    .then(response => response.json())
    .then(jsonData =>{
      console.log(jsonData)
      const locations = jsonData.locations.map(object => (object)) //this is an object with an array in it
      this.setState({locations})
    })
  }

  render(){
    return( 
      <div className="offset-md-4 col-md-4">
        <h4 align="center"> Location </h4>
        <ListGroup>
          {this.state.locations.map((locations, index) =>
            <ListGroupItem key={index}> {locations} </ListGroupItem>
          )}
        </ListGroup>
    </div>);
  }

}


