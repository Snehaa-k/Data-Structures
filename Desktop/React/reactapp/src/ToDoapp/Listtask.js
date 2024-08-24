import React from 'react'
import { Button } from 'react-bootstrap'
import { useState } from 'react'

const Listtask = ({task,index,removeTask,taskCompletion}) => {
  const handleCheckbox = () => {
    taskCompletion(index);
  };
  return (
    <>

    <div className='list-taks d-flex justify-content-between align-items-center'>
      <input    type='checkbox'  onChange = {handleCheckbox} checked = {task.completed} style={{ transform: 'scale(1.5)' }}/>
      <span style={{ textDecoration: task.completed ? 'line-through' : 'none',  textDecorationColor:'black'}}>
        {task.title}
      </span>
        <Button onClick={()=>{removeTask(index)}} className='btn btn-danger m-2'>Delete</Button>
        
        
    </div>
    {/* {task.completed && <div><h5>The Task</h5>{task.title}<h5>completed</h5></div>} */}
    
    </>
  )
}

export default Listtask