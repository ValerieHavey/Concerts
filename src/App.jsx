import { useState, useEffect } from "react";
import './App.css'
import axios from "axios";

function App() {
  const [count, setCount] = useState(0);
  const [array, setArray] = useState([]);

  const fetchAPI = async () => {
    const response = await axios.get("http://localhost:8080/concerts/users");
    setArray(response.data.users);
  };


  useEffect(() => {
    fetchAPI();
  }, []);


  return (
    <>
    <h1>Hello world!</h1>
    </>
  )
}

export default App;
