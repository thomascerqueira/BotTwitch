import { createContext, useContext } from "react";
import { ICommand } from "./interfaces/ICommand";


interface ICommandProvider {
    commands: { [key: string]: ICommand },
    setCommands: React.Dispatch<React.SetStateAction<any | null>>
}

export const CommandsProvider = createContext<ICommandProvider | null>(null)

export const useCommandsProvider = () => {
    const context = useContext(CommandsProvider)
    if (!context) {
        throw new Error("useCommandsProvider must be used within a CommandsProvider")
    }
    return context
}