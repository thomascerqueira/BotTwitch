import React from "react"
import "./command.css"
import axios from 'axios'
import { SERVER_URL } from './config'
import { Command } from "./Widgets/commands/Command"
import { useCommandsProvider } from "./Provider"

export default function Commands() {
  const {commands, setCommands} = useCommandsProvider()

  function onChangeInput(e: any, key: string, keyValue: string) {
    setCommands({
      ...commands,
      [key]: {
        ...commands[key],
        data: {
          ...commands[key].data,
          [keyValue]: e.target.value
        }
      }
    })
  }

  function deleteCommand(command: string) {
    axios.delete(SERVER_URL + "commands/" + command)
    .then(() => {
      const _commands = {...commands}
      delete _commands[command]
      setCommands(_commands)
    })
  }

  return (
    <>
      <div className="commands">
        <div className="header">
          <h1 className="command">
            Commands
          </h1>
          <h1 className="description">
            Description
          </h1>
          <h1 className="arguments">
            Arguments
          </h1>
        </div>

        <div className="body">
          {
            commands && Object.entries(commands).map(
              ([key, value]) => {
                return (
                  <Command
                    key={key}
                    command={key}
                    value={value}
                    onChangeInput={onChangeInput}
                    deleteCommand={deleteCommand}
                  />
                )
              })
          }
        </div>
      </div>
    </>
  )
}