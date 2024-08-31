package main

import (
    "fmt"
    "errors"
)

func main() {
    myStruct := user{
        "Arbab",
        "Ansari",
        true,
    }

    myProduct := product{
        "iPad",
        999,
    }

    val, err := modifyStruct(myStruct)
    if err != nil {
        fmt.Println(err)
    } else {
        fmt.Println(val)
    }

    val2, err2 := modifyStruct(myProduct)
    if err2 != nil {
        fmt.Println(err2)
    } else {
        fmt.Println(val2)
    }
}

func modifyStruct[T stringer] (s T) (string, error) {
    if s.isPremium() == false {
        var zeroVal string
        return zeroVal, errors.New("Premium feature requested!")
    }
    return s.getString(), nil
}

type stringer interface {
    getString() string
    isPremium() bool
}

type user struct {
    firstName string
    lastName string
    isSubscribed bool
}

func (u user) getString() string {
    return u.firstName + " " + u.lastName
}

func (u user) isPremium() bool {
    return u.isSubscribed
}

type product struct {
    productName string
    productCost int
}

func (p product) getString() string {
    return p.productName
}

func (p product) isPremium() bool {
    if p.productCost > 100 {
        return true
    }
    return false
}
