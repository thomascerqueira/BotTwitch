import React from "react";
import Dropdown from 'react-dropdown';
import 'react-dropdown/style.css';
import "./CreateCommand.css"

interface Props {
    availableFunctions: {
        [key: string]: {
            args: { [key: string]: string },
            description: string
        }
    }
}

export default function CreateCommand(
    {
        availableFunctions
    }: Props
) {
    const [selectedFunction, setSelectedFunction] = React.useState("")
    const [availableChoices, setAvailableChoices] = React.useState<{ label: string, value: string }[]>([])

    React.useEffect(() => {
        const test = (Object.entries(availableFunctions).map(
            ([func, value]) => {
                return {
                    value: func,
                    label: `${func}: ${value.description}`
                }
            }
        ))

        console.log(test)
        setAvailableChoices(test)
    }, [availableFunctions])

    return (
        <>
            <div className="create-command">
                <Dropdown
                    className="dropdown"
                    options={availableChoices}
                    value={selectedFunction}
                    onChange={(e: { value: React.SetStateAction<string>; }) => {
                        setSelectedFunction(e.value)
                    }}
                />
                {
                    selectedFunction !== "" && (
                        <div>
                            oui
                            </div>
                    )
                }
            </div>
        </>
    )
}