import React, { Component } from 'react';
import axios from 'axios';

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
      <div className="App">
        <form onSubmit={this.handleSubmit}>
          <p>
            <input type="text" placeholder='Name' id='name' value={this.state.name} onChange={this.handleChange} required/>
          </p>
          <p>
            <input type="text" placeholder='Surname' id='surname' value={this.state.surname} onChange={this.handleChange} required/>

          </p>
          <p>
            <input type="file"
                   id="id_image"
                   accept="image/png, image/jpeg"  onChange={this.handleIdImageChange} required/>
          </p>

          <p>
            <input type="file"
                   id="selfie_image"
                   accept="image/png, image/jpeg"  onChange={this.handleSelfieImageChange} required/>
          </p>
          <input type="submit"/>
        </form>
      </div>
    );
  }
}

export default App;