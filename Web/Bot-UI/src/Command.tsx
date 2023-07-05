import "./Command.css"

interface ICommand {
  function: string,
  args: any,
  description: string
}

interface Props {
  commands: { [key: string]: ICommand }
}

export default function Commands(
  {
    commands
  }: Props
) {
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
            Object.keys(commands).map((key) => {
              const command = commands[key]

              return (
                <div className="command">
                  <div className="function">
                    {key}
                  </div>
                  <div className="description">
                    {command.description}
                  </div>
                  <div className="args">
                    {
                      Object.keys(command.args).map((arg) => {
                        return (
                          <div className="arg">
                            <p className="arg-name">
                              {
                                `${arg}:`
                              }
                            </p>
                            <p className="arg-type">
                              {
                              command.args[arg]
                              }
                            </p>
                          </div>
                        )
                      })
                    }
                  </div>
                </div>
              )
            })
          }
        </div>
      </div>
    </>
  )
}