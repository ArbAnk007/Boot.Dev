package main

import (
    "fmt"

    "time"
)

func main() {
    example()
    anotherExample()
    oneMoreExample()
}

func example() {
    ch := make(chan int)
    var myVar int
    go func() {
        fmt.Println("This runs 03")
        myVar = <- ch
    }()
    time.Sleep(time.Second)
    fmt.Println("This runs 01")
    ch <- 5
    fmt.Println("This runs 02")
    fmt.Println(myVar)
}

func anotherExample() {
    ch := make(chan int)
    go func() {
        ch <- 10
    }()
    fmt.Println(<-ch)
}

func oneMoreExample() {
    ch := make(chan int, 100)
    ch <- 10
    ch <- 12
    fmt.Println(<-ch)
    fmt.Println(<-ch)
}
