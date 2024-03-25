import React from 'react'
import axios from 'axios'
import { SERVER_URL } from '../../config'

interface Props {
    refreshCommands: () => void
}

export function AddCommand(
    {
        refreshCommands
    }: Props
) {
    const [args, setArgs] = React.useState<{ [key: string]: string }>({})
    const [description, setDescription] = React.useState('')
    const [command, setCommand] = React.useState('')
    const [file, setFile] = React.useState<File | null>(null)

    function onFileChange(event: any) {
        const file = event.target.files[0]
        if (!file || !file.name.endsWith('.py')) {
            return
        }
        const pattern = /kwargs\.get\(\s*["']((?!commandTrigger)[^'"]+)["']/g;

        const reader = new FileReader()
        reader.onload = (e) => {
            const text = (e.target?.result as string)
            let result;
            let _args: { [key: string]: string } = {}

            while ((result = pattern.exec(text)) !== null) {
                _args[result[1]] = ''
            }

            setArgs(_args)
        }
        reader.readAsText(file)
        setFile(file)
    }


    return (
        <>
            <div>
                <h1>Add Command</h1>
                <div>
                    <input
                    placeholder="Command"
                    value={command}
                    onChange={(e) => {
                        setCommand(e.target.value)
                    }}
                    />
                    <input
                    placeholder="Description"
                    value={description}
                    onChange={(e) => {
                        setDescription(e.target.value)
                    }}
                    />
                </div>
                <div>
                    {
                        Object.entries(args)
                        .map(([key, _]) => {
                            return (
                                <div key={key}>
                                    <p>
                                        {key}
                                    </p>
                                    <input
                                        placeholder=""
                                        onChange={(e) => {
                                            setArgs({
                                                ...args,
                                                [key]: e.target.value
                                            })
                                        }}
                                    />
                                </div>
                            )
                        })
                    }
                </div>
                <input
                    type="file"
                    accept=".py"
                    onChange={onFileChange}
                />
                <div>
                    <button
                    onClick={() => {
                        if (!command || !file) {
                            return
                        }
                        const _command = command.replace("!", '')

                        const data = {
                            description: description,
                            file: file.name,
                            data: args
                        }

                        axios.post(SERVER_URL + "commands/" + _command, data)
                        .finally(() => {
                            refreshCommands()
                        })
                    }}
                    >
                        Add
                    </button>
                </div>
            </div>
        </>
    )
}