import { useState } from "react";
import ReactDOM from "react-dom";

function MyLogin(){
  const [inputs, setInputs] =useState({});

  const handleInputChange = (event) => {
    const name=event.target.name;
    const value=event.target.value;
    setInputs({...inputs, [name]: value });
    console.log(inputs);

  }
  const handleSubmit = (event) => {
    event.preventDefault();
    alert(inputs);
    // submit form data here
  }
  return (
    <form onSubmit={handleSubmit}>
      <label>Enter your name
      <input type="text"
      name="username"
      value={inputs.username}

        onChange={handleInputChange} />
      </label>
      <label>
        Enter your password
        <input type="password"
        name="password"
        value={inputs.password}
        onChange={handleInputChange} />
      </label>
      <label>
        Enter your email
        <input type="email"
        name="email"
        value={inputs.email}
        onChange={handleInputChange} />
      </label>
      <input type="submit" value="Submit" />
    </form>
  )
}
const root=ReactDOM.createRoot(document.getElementById('root'));

root.render(<MyLogin />);     