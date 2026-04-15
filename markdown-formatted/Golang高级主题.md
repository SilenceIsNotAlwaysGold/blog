---
title: "Golang高级主题"
summary: "并发编程 goroutines channels select语句 包和依赖管理 导入和使用标准库 第三方包管理（使用go mod） **初始化模块**： **导入第三方包**： **下载依赖**： 测试 编写单元测试（testing包） **源代码**： **测试代码**： **运行测试**： 基准测试 **源代码**： **基准测试代码**： **运行基..."
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

### 并发编程
#### goroutines
```go
package main

import (
    "fmt"
    "time"
)

func sayHello() {
    fmt.Println("Hello")
}

func main() {
    go sayHello()
    time.Sleep(1 * time.Second) // 确保goroutine有时间执行
    fmt.Println("Main function")
}
```

#### channels
```go
package main

import (
    "fmt"
)

func main() {
    messages := make(chan string)

    go func() {
        messages <- "ping"
    }()

    msg := <-messages
    fmt.Println(msg)
}
```

#### select语句
```go
package main

import (
    "fmt"
    "time"
)

func main() {
    chan1 := make(chan string)
    chan2 := make(chan string)

    go func() {
        time.Sleep(1 * time.Second)
        chan1 <- "one"
    }()

    go func() {
        time.Sleep(2 * time.Second)
        chan2 <- "two"
    }()

    for i := 0; i < 2; i++ {
        select {
        case msg1 := <-chan1:
            fmt.Println("received", msg1)
        case msg2 := <-chan2:
            fmt.Println("received", msg2)
        }
    }
}
```

### 包和依赖管理
#### 导入和使用标准库
```go
package main

import (
    "fmt"
    "math"
)

func main() {
    fmt.Println("Pi:", math.Pi)
}
```

#### 第三方包管理（使用go mod）
1. **初始化模块**：

```shell
go mod init example.com/mymodule
```

2. **导入第三方包**：

```go
package main

import (
    "fmt"
    "github.com/google/uuid"
)

func main() {
    id := uuid.New()
    fmt.Println("UUID:", id)
}
```

3. **下载依赖**：

```shell
go mod tidy
```

### 测试
#### 编写单元测试（testing包）
1. **源代码**：

```go
package main

func Add(a, b int) int {
    return a + b
}
```

2. **测试代码**：

```go
package main

import "testing"

func TestAdd(t *testing.T) {
    result := Add(2, 3)
    if result != 5 {
        t.Errorf("Add(2, 3) = %d; want 5", result)
    }
}
```

3. **运行测试**：

```shell
go test
```

#### 基准测试
1. **源代码**：

```go
package main

func Add(a, b int) int {
    return a + b
}
```

2. **基准测试代码**：

```go
package main

import "testing"

func BenchmarkAdd(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Add(2, 3)
    }
}
```

3. **运行基准测试**：

```shell
go test -bench=.
```

这些示例涵盖了Golang的高级主题，帮助你掌握并发编程、包管理和测试的基本知识。如果你有任何进一步的问题或需要更多示例，请告诉我！
