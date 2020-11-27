import React, { useState, useEffect } from 'react'
import { Display } from './display';


var j; 
export const List = () => {
    // var [li, setList] = useState([]);
    // useEffect(() => {
    //     setList("test")
    //     fetch('/list').then(response => {
    //         j = response.json();
    //     }).then(data => setList(data))
    //     console.log(li)
    // }, [])
    const j = [
        {test: "test"}
    ];
    
    fetch('/list').then(response => {
        if (response.ok) {
            var x = response.json();
            x.then(function(result) {
                j.push(result);
            });
        }
    })
    return (
        <>
            {j.map(l => {
                return(
                    <ul key = {l.id}>
                        <li>{l.content}</li>
                    </ul>
                )
            })}
        </>
    )
   
    
}