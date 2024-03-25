import React, { useCallback } from 'react'
import axios from 'axios'
import { SERVER_URL } from './config'
import Commands from './Commands'
import { AddCommand } from './Widgets/addCommands/AddCommand'
import { CommandsProvider } from './Provider'

function App() {
  const [commands, setCommands] = React.useState({})

  const refreshCommands = useCallback(() => {
    axios.get(SERVER_URL + "commands").then((res) => {
      setCommands(res.data)
    })
  }, [setCommands])

  React.useEffect(() => {
    refreshCommands()
  }, [])

  return (
    <CommandsProvider.Provider value={
      {
        commands,
        setCommands
      }
    }>
      <div>
        <Commands/>
        <button onClick={() => {
          axios.get(SERVER_URL + "commands").then((res) => {
            setCommands(res.data)
          })
        }}>
          Refresh
        </button>
        <AddCommand
          refreshCommands={refreshCommands}
        />
      </div>
    </CommandsProvider.Provider>
  )
}

export default App
