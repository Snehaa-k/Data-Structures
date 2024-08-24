import {Button} from 'react-bootstrap';
import React, { useState } from 'react'
import Swal from 'sweetalert2';

const Addtask = ({addTask}) => {
  const [value,setValue] = useState("");
  const additem = ()=>{
    // console.log(value)
    const trimmedvalue = value.trim()
    if(trimmedvalue !== "")
      {

        addTask(trimmedvalue);
        setValue(" ");
        Swal.fire({
          icon: 'success',
          title: 'Task Added!',
          text: 'Your task has been successfully added.',
        });

      }
    else
    {
      Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: 'Please enter a task!',
      });
    }
   
 
  }
  return (
    <>
    <div className='input-container col-md-6 offset-md-3 d-flex align-items-center'>
    <input  type='text'  value = {value} onChange={(e)=>{setValue(e.target.value)}} class='form-control custom-input' placeholder='Add Your Task' required/>
    
   
    <Button onClick={additem} className='btn btn-warning m-2'>ADD</Button>
    </div>
    </>
  )
}

export default Addtask