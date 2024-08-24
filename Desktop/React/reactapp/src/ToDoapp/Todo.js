import React, { useEffect, useState } from 'react'
import "./Todo.css";
import Addtask from './Addtask'
import Listtask from './Listtask'

const Todo = () => {
  const [samplelist,setTask] = useState([
   
  ]);
  useEffect(()=>{
    document.title = `you have ${samplelist.length} pending tasks(s)`
  })
  
  const addTask = (title)=>{
       
      const newTask = [...samplelist,{title,completed:false}];
       
       
        setTask(newTask)
              
  };
  const removeTask = (index)=>{
    const newTask = [...samplelist]
    newTask.splice(index,1)
    setTask (newTask)
  }
  const taskCompletion = (index) => {
    const newTasks = [...samplelist];
    newTasks[index].completed = !newTasks[index].completed;
    setTask(newTasks);
  };
  return (
    <>
        <div className='todo-container '>
            <div className='header'>
              <h1 >TO-DO LIST</h1>
              </div>
            <div className='add-task'>
              <Addtask addTask = {addTask}/>
            </div>
            <div className='task'>
              {samplelist.map((task,index)=>(
                <Listtask task={task} removeTask={removeTask}  index = {index}  taskCompletion={taskCompletion}/>

              ))}
           
            </div>
           
        </div>
    </>
  );
};

export default Todo