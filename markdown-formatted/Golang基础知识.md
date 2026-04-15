---
title: "Golang基础知识"
summary: "变量和常量 变量 常量 基本数据类型 整数、浮点数、布尔值、字符串 复合数据类型 数组 切片 字典（映射） 结构体 指针 函数和方法 函数 方法 接口 控制结构 条件语句（if、switch） 循环语句（for） 错误处理 error类型 自定义错误"
board: "tech"
category: "编程语言-Golang"
tags:
  - "Golang"
  - "Go"
  - "编程"
author: "博主"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---

### 变量和常量
#### 变量
```go
package main

import "fmt"

func main() {
    var a int = 10
    var b = 20 // 类型推断
    c := 30    // 简短声明

    fmt.Println(a, b, c)
}
```

#### 常量
```go
package main

import "fmt"

const Pi = 3.14
const (
    A = 1
    B = 2
)

func main() {
    fmt.Println(Pi, A, B)
}
```

### 基本数据类型
#### 整数、浮点数、布尔值、字符串
```go
package main

import "fmt"

func main() {
    var i int = 42
    var f float64 = 3.14
    var b bool = true
    var s string = "Hello, Go"

    fmt.Println(i, f, b, s)
}
```

### 复合数据类型
#### 数组
```go
package main

import "fmt"

func main() {
    var arr [5]int = [5]int{1, 2, 3, 4, 5}
    fmt.Println(arr)
}
```

#### 切片
```go
package main

import "fmt"

func main() {
    var slice []int = []int{1, 2, 3, 4, 5}
    slice = append(slice, 6)
    fmt.Println(slice)
}
```

#### 字典（映射）
```go
package main

import "fmt"

func main() {
    var dict map[string]int = map[string]int{"one": 1, "two": 2}
    dict["three"] = 3
    fmt.Println(dict)
}
```

#### 结构体
```go
package main

import "fmt"

type Person struct {
    Name string
    Age  int
}

func main() {
    var p Person = Person{Name: "Alice", Age: 25}
    fmt.Println(p)
}
```

### 指针
```go
package main

import "fmt"

func main() {
    var a int = 42
    var p *int = &a

    fmt.Println(a, p, *p)
}
```

### 函数和方法
#### 函数
```go
package main

import "fmt"

func add(a int, b int) int {
    return a + b
}

func main() {
    result := add(3, 4)
    fmt.Println(result)
}
```

#### 方法
```go
package main

import "fmt"

type Person struct {
    Name string
}

func (p Person) Greet() {
    fmt.Println("Hello, my name is", p.Name)
}

func main() {
    var p Person = Person{Name: "Bob"}
    p.Greet()
}
```

### 接口
```go
package main

import "fmt"

type Speaker interface {
    Speak()
}

type Person struct {
    Name string
}

func (p Person) Speak() {
    fmt.Println("Hello, I am", p.Name)
}

func main() {
    var s Speaker = Person{Name: "Charlie"}
    s.Speak()
}
```

### 控制结构
#### 条件语句（if、switch）
```go
package main

import "fmt"

func main() {
    var num int = 10

    if num > 5 {
        fmt.Println("Greater than 5")
    } else {
        fmt.Println("Less than or equal to 5")
    }

    switch num {
    case 10:
        fmt.Println("Ten")
    case 20:
        fmt.Println("Twenty")
    default:
        fmt.Println("Unknown number")
    }
}
```

#### 循环语句（for）
```go
package main

import "fmt"

func main() {
    for i := 0; i < 5; i++ {
        fmt.Println(i)
    }

    var j int = 0
    for j < 5 {
        fmt.Println(j)
        j++
    }
}
```

### 错误处理
#### error类型
```go
package main

import (
    "errors"
    "fmt"
)

func main() {
    var err error = errors.New("an error occurred")
    fmt.Println(err)
}
```

#### 自定义错误
```go
package main

import (
    "fmt"
)

type MyError struct {
    Message string
}

func (e *MyError) Error() string {
    return e.Message
}

func mightFail(flag bool) error {
    if flag {
        return &MyError{Message: "something went wrong"}
    }
    return nil
}

func main() {
    err := mightFail(true)
    if err != nil {
        fmt.Println(err)
    }
}
```
