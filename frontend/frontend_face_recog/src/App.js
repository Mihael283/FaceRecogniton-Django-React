import React, { Component } from 'react';
import axios from 'axios';
import Button from 'react-bootstrap/Button'
import 'bootstrap/dist/css/bootstrap.min.css'

import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Stack from 'react-bootstrap/Stack';

class App extends Component {

  state = {
    name: '',
    surname: '',
    id_image: null,
    selfie_image: null,
  };

  handleChange = (e) => {
    this.setState({
      [e.target.id]: e.target.value
    })
  };

  handleIdImageChange = (e) => {
    this.setState({
      id_image: e.target.files[0]
    })
  };

  handleSelfieImageChange = (e) => {
    this.setState({
      selfie_image: e.target.files[0]
    })
  };

  check = (e) =>{
    console.log("AAA")
  }

  handleSubmit = (e) => {
    e.preventDefault();
    console.log(this.state);
    let form_data = new FormData();
    form_data.append('name', this.state.name);
    form_data.append('surname', this.state.surname);
    form_data.append('id_image', this.state.id_image, this.state.id_image.name);
    form_data.append('selfie_image', this.state.selfie_image, this.state.selfie_image.name);
    let url = 'http://localhost:8000/profile/register/';
    axios.post(url, form_data, {
      headers: {
        'content-type': 'multipart/form-data'
      }
    })
        .then(res => {
          console.log(res.data);
        })
        .catch(err => console.log(err))
  };

  render() {
    return (
      <Stack gap={2} className="col-md-5 mx-auto">
      <div className="App">
        <Form onSubmit={this.handleSubmit}>
          <Form.Group className="mb-3" controlId="name" >
            <Form.Label>Name</Form.Label>
            <Form.Control type="text" placeholder="Enter Name" id = "name" value={this.state.name} onChange={this.handleChange} required/>
          </Form.Group>

          <Form.Group className="mb-3" controlId="surname" value={this.state.surname}>
            <Form.Label>Surname</Form.Label>
            <Form.Control type="text" placeholder="Enter Surname" id = "surname" value={this.state.surname} onChange={this.handleChange} required/>
          </Form.Group>

          <Form.Group className="mb-3" controlId="id_image" accept="image/png, image/jpeg">
            <Form.Label>ID Image</Form.Label>
            <Form.Control type="file" placeholder="Upload ID Image" id = "id_image" onChange={this.handleIdImageChange} required/>
          </Form.Group>

          <Form.Group className="mb-3" controlId="selfie_image" accept="image/png, image/jpeg">
            <Form.Label>Selfie Image</Form.Label>
            <Form.Control type="file" placeholder="Upload Selfie Image" id = "selfie_image" onChange={this.handleSelfieImageChange} required/>
          </Form.Group>

          <Button variant="primary" type="submit">
            Submit
          </Button>
        </Form>
      </div>
      </Stack>
    );
  }
}

export default App;