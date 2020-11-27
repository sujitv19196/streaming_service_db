import logo from './logo.svg';
import './App.css';
import { Delete } from './delete.js';
import { List } from './list';
import {useState} from 'react'
import react from 'react';

function App() {
  const [record, setRecord] = useState('')

  const handleFormChange = (inputValue) => {
    setRecord(inputValue);
    console.log(record);
  }

  const handleFormSubmit = (action) => {
    fetch(`/search?name=${record}`)
  }
  const handleFormDelete = (action) => {
    fetch(`/delete?name=${record}`)
  }
  const handleFormInset = (action) => {
    fetch(`/insert?name=${record}`)
  }
  const handleFormUpdate = (action) => {
    var arr = record.split(" ");
    var name = arr[0]
    var year = arr[1]
    fetch(`/update?name=${name}&?year=${year}`)
  }
  
  
  return (
    <div className="App">
      Team Tired
      <Delete userInput = {record} onFormChange = { handleFormChange } onFormSubmit = {handleFormSubmit} onFormDelete = {handleFormDelete} onFormInsert = {handleFormInset} onFormUpdate = {handleFormUpdate}/> 
      {/* <List/>  */}
    </div>
  );
}

export default App;
