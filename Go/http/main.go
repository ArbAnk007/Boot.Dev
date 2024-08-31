package main

import (
	//"encoding/json"
	"fmt"
	"io"
	"net/http"
    //"time"
)

func main() {
    url := "https://api.github.com/users/arbank007"
    getData(url)
}

func getData(url string) string {
    res, err := http.Get(url)
    if err != nil {
        fmt.Println("Error retrieving data: ", err)
        return "Failed"
    }
    fmt.Println(res.Body)
    data, readErr := io.ReadAll(res.Body)
    defer res.Body.Close()
    if readErr != nil {
        fmt.Println("Error reading body: ", readErr)
        return "Failed"
    }
    fmt.Println(string(data))
    return "success"
}
