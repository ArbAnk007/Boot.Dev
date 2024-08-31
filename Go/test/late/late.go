package late

import (
    "fmt"
    "time"
)

func RunLate() {
    time.Sleep(3 * time.Second)
    fmt.Println("Hello this function is running late")
}
