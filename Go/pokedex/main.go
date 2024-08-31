package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"

	"github.com/arbank007/pokedex-cli/internal/pokecache"
)

func main() {
    pokeCache := pokecache.NewCache()
    commands := map[string]cliCommand{
        "help": {"help", "This is help command", commandHelp},
        "exit": {"exit", "This is exit command", commandExit},
    }

    config := Config{0, "https://pokeapi.co/api/v2/location-area", nil}
    caughtPokemon := []string{}
    
    scanner := bufio.NewScanner(os.Stdin)
    running := true
    for running {
        fmt.Print("Enter command: ")
        scanner.Scan()
        command := scanner.Text()
        var region string
        var pokemon string
        commandSlice := strings.Split(command, " ")
        if len(commandSlice) == 2 && commandSlice[0] == "explore" {
            command = commandSlice[0]
            region = commandSlice[1]
        } else if len(commandSlice) == 2 && commandSlice[0] == "catch" {
            command = commandSlice[0]
            pokemon = commandSlice[1]
        }

        if command == "help" {
            commands["help"].callback()
        } else if command == "exit" {
            commands["exit"].callback()
            running = false
        } else if command == "map" {
            commandMap(&config, &pokeCache)
        } else if command == "mapb" {
            commandMapb(&config, &pokeCache)
        } else if command == "page" {
            commandPage(&config)
        } else if command == "clear" {
            commandClear()
        } else if command == "explore" {
            err := commandExplore(region, &pokeCache)
            if err != nil {
                fmt.Println("Something went wrong: ", err)
            }
        } else if command == "catch" {
            err := commandCatch(pokemon, &caughtPokemon)
            if err != nil {
                fmt.Println("Something went wrong: ", err)
            }
        } else if command == "pokemon" {
            commandPokedex(caughtPokemon)
        } else {
            fmt.Println("Invalid command!")
            fmt.Println("Enter help for list of commands")
        }
    }
}