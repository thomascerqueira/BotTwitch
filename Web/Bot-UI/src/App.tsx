import React from 'react'
import axios from 'axios'
import { SERVER_URL } from './config'
import Commands from './Command'
import CreateCommand from './CreateCommand'

function App() {
  const [commands, setCommands] = React.useState({})
  const [functions, setFunctions] = React.useState({})

  React.useEffect(() => {
    axios.get(SERVER_URL + "command").then((res) => {
      setCommands(res.data.commands)
    })
  }, [])

  React.useEffect(() => {
    axios.get(SERVER_URL + "functions").then((res) => {
      setFunctions(res.data.functions)
    })
  }, [])


  return (
    <>
      <div>
        On est la
        <Commands commands={commands}/>
        <CreateCommand availableFunctions={functions}/>
      </div>
    </>
  )
}

export default App
