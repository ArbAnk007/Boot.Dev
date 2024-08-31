package main

import (
	"encoding/json"
	"fmt"
	"math/rand"
	"net/http"

	"github.com/arbank007/pokedex-cli/internal/pokecache"
)

func commandHelp() error {
	fmt.Println("**********This is the help page**********")
	fmt.Println("Available commands:")
	fmt.Println("help -- Displays the list of commands")
	fmt.Println("map -- Lists name of next 20 location")
	fmt.Println("mapb -- Lists name of previous 20 location")
	fmt.Println("page -- Lists the page number")
	fmt.Println("catch <POKEMON> -- Throws a pokeball to catch <POKEMON>")
	fmt.Println("pokedex -- Lists all the caught pokemon")
	fmt.Println("explore <AREA-NAME> -- Lists all the pokemon available in the area")
	fmt.Println("clear -- Clear the screen")
	fmt.Println("exit -- Exits the program")
	return nil
}

func commandExit() error {
	fmt.Println("Thanks for using PokeDex!")
	return nil
}

func commandMap(c *Config, cache *pokecache.Cache) error {
	url, ok := c.next.(string)
	if !ok {
		fmt.Println("You are on last page!")
		return fmt.Errorf("EOF")
	}

	val, is_cached := cache.Get(url)
	if is_cached {
		var data Data
		err := json.Unmarshal(val, &data)
		if err != nil {
			fmt.Println("Something went wrong!", err)
			return err
		}

		// Updating config
		c.prev = data.Previous
		c.next = data.Next
		c.page += 1

		for _, location := range data.Results {
			fmt.Println(location.Name)
		}

		return nil
	}

	// Making request
	res, err := http.Get(url)
	if err != nil {
		fmt.Println("Error occured in making request: ", err)
		return err
	}

	// Decoding the data
	var data Data
	decoder := json.NewDecoder(res.Body)
	err = decoder.Decode(&data)
	if err != nil {
		fmt.Println("Error occured in decoding data: ", err)
		return err
	}

	// Caching the data
	val, err = json.Marshal(data)
	if err != nil {
		fmt.Println("Something went wrong!", err)
		return err
	}
	cache.Add(url, val)

	// Updating config
	c.prev = data.Previous
	c.next = data.Next
	c.page += 1

	for _, location := range data.Results {
		fmt.Println(location.Name)
	}

	return nil
}

func commandMapb(c *Config, cache *pokecache.Cache) error {
	url, ok := c.prev.(string)
	if !ok {
		fmt.Println("You are on first page!")
		return fmt.Errorf("EOF")
	}

	val, is_cached := cache.Get(url)
	if is_cached {
		var data Data
		err := json.Unmarshal(val, &data)
		if err != nil {
			fmt.Println("Something went wrong!", err)
			return err
		}

		// Updating config
		c.prev = data.Previous
		c.next = data.Next
		c.page -= 1

		for _, location := range data.Results {
			fmt.Println(location.Name)
		}

		return nil
	}

	// Making request
	res, err := http.Get(url)
	if err != nil {
		fmt.Println("Error occured in making request: ", err)
		return err
	}

	// Decoding the data
	var data Data
	decoder := json.NewDecoder(res.Body)
	err = decoder.Decode(&data)
	if err != nil {
		fmt.Println("Error occured in decoding data: ", err)
		return err
	}

	// Caching the data
	val, err = json.Marshal(data)
	if err != nil {
		fmt.Println("Something went wrong!", err)
		return err
	}
	cache.Add(url, val)

	// Updating cofig
	c.prev = data.Previous
	c.next = data.Next
	c.page -= 1

	for _, location := range data.Results {
		fmt.Println(location.Name)
	}

	return nil
}

func commandExplore(region string, cache *pokecache.Cache) error {
	baseUrl := "https://pokeapi.co/api/v2/location-area/"
	fullUrl := baseUrl + region

	// Check in cache
	val, is_cached := cache.Get(fullUrl)
	if is_cached {
		var locationData Location
		err := json.Unmarshal(val, &locationData)
		if err != nil {
			fmt.Println("Somethin went wrong: ", err)
			return err
		}

		// Displaying data
		fmt.Printf("Exploring %s...\nFound Pokemon:\n", region)
		for _, val := range locationData.PokemonEncounters {
			fmt.Println("  -",val.Pokemon.Name)
		}
		return nil

	}

	// Making request
	res, err := http.Get(fullUrl)
	if err != nil {
		return err
	}

	if res.StatusCode == 404 {
		return fmt.Errorf("invalid area")
	}

	// Decoding data
	var locationData Location
	defer res.Body.Close()
	decoder := json.NewDecoder(res.Body)
	err = decoder.Decode(&locationData)
	if err != nil {
		return err
	}

	// Caching the data
	val, err = json.Marshal(locationData)
	if err != nil {
		return err
	}
	cache.Add(fullUrl, val)

	// Displaying the data
	fmt.Printf("Exploring %s...\nFound Pokemon:\n", region)
	for _, val := range locationData.PokemonEncounters {
		fmt.Println("  -",val.Pokemon.Name)
	}
	return nil
}

func commandCatch(name string, catchedPokemon *[]string) error {
	for _, pokemon := range *catchedPokemon {
		if name == pokemon {
			fmt.Println(name, " already caught!")
			return nil
		}
	}
	baseUrl := "https://pokeapi.co/api/v2/pokemon/"
	fullUrl := baseUrl+name
	
	res, err := http.Get(fullUrl)
	if err != nil {
		return err
	}
	if res.StatusCode == 404 {
		return fmt.Errorf("invalid pokemon")
	}

	var pokemon Pokemon
	defer res.Body.Close()
	decoder := json.NewDecoder(res.Body)
	err = decoder.Decode(&pokemon)
	if err != nil {
		return err
	}

	fmt.Println("Throwing a pokeball at ", pokemon.Name, "...")
	if rand.Intn(pokemon.BaseExperience) < 10 {
		*catchedPokemon = append(*catchedPokemon, pokemon.Name)
		fmt.Println(pokemon.Name," was caught!")
		return nil
	}

	fmt.Println(pokemon.Name, " escaped!")
	return nil
}

func commandPokedex(caughtPokemon []string) {
	if len(caughtPokemon) == 0 {
		fmt.Println("No pokemon caught yet!")
		return
	}
	for _, pokemon := range caughtPokemon {
		fmt.Println("  -", pokemon)
	}
}

func commandPage(c *Config) {
	fmt.Println(c.page)
}

func commandClear() {
	fmt.Print("\033[H\033[2J")
}