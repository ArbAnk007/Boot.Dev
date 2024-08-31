package main

import (
    "fmt"
) 

func main() {
    ch := make(chan int)
    ch <- 5
    var v int
    v = <- ch
    fmt.Println(ch)
    fmt.Println(v)
}
