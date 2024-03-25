import axios from 'axios';
import { ICommand } from '../../interfaces/ICommand';
import { SERVER_URL } from '../../config';
import { useCommandsProvider } from '../../Provider';

interface Props {
  onChangeInput: any,
  command: string,
  value: ICommand,
  deleteCommand: any
}

export function Command(
  {
    command,
    value,
    onChangeInput,
    deleteCommand
  }: Props
) {
  const { commands } = useCommandsProvider()

  return (
    <div className="command">
      <div className="function">
        {command}
      </div>
      <div className="description">
        {value.description}
      </div>
      <div className="args">
        {
          value.data && Object.entries(value.data).map(
            ([keyValue, value]) => {
              return (
                <div className="arg" key={keyValue}>
                  <p>
                    {keyValue}
                  </p>
                  <input
                    className="type"
                    value={value as string}
                    onChange={(e) => {
                      onChangeInput(e, command, keyValue)
                    }}
                  />
                </div>
              )
            }
          )
        }
      </div>
      <button
        onClick={() => {
          axios.patch(
            SERVER_URL + "commands/" + command,
            commands[command]
          )
        }}
      >
        Save
      </button>
      <button
        onClick={() => {
          deleteCommand(command)
        }}
      >
        Delete
      </button>
    </div>
  )
}