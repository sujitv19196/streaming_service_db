import React from 'react'

export const Delete = ({userInput, onFormChange, onFormSubmit, onFormDelete, onFormInsert, onFormUpdate}) => {
    const deleteRecord = () => {
        fetch(`/delete/cs411`)
    } 
    const handleChange = (event) => {
        onFormChange(event.target.value);
    }
    const handleSubmit = (event) => {
        event.preventDefault()
        onFormSubmit();
    } 

    const handleDelete = (event) => {
        event.preventDefault()
        onFormDelete();
    } 

    const handleInsert = (event) => {
        event.preventDefault()
        onFormInsert();
    } 

    const handleUpdate = (event) => {
        event.preventDefault()
        onFormUpdate();
    } 

    return (
    <>
        <form onSubmit = {handleSubmit}>
            <input type = "text" required value={userInput} onChange = {handleChange}/>
            <input type = "submit"/>
            <button type = "button" onClick={handleDelete}> delete </button>
            <button type = "button" onClick={handleInsert}> insert </button>
            <button type = "button" onClick={handleUpdate}> update </button>
        </form> 
    </>
    )
}