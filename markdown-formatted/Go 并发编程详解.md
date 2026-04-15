---
title: "Go 并发编程详解"
summary: "深入理解 Go 语言的并发模型，掌握 Goroutine 的调度原理、Channel 的通信机制以及 Sync 包的同步原语，编写高效的并发程序。"
board: "tech"
category: "编程语言-Golang"
tags:
  - "Go"
  - "Golang"
  - "并发"
  - "Goroutine"
cover_image: ""
author: "博主"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---

# Go 并发编程详解

Go 语言最大的亮点之一就是其原生支持并发。通过 Goroutine 和 Channel，Go 让并发编程变得简单而优雅。本文将深入探讨 Go 的并发模型（GMP）及其实战用法。

## 1. Goroutine：轻量级线程

Goroutine 是 Go 运行时管理的轻量级线程。启动一个 Goroutine 非常简单，只需在函数调用前加上 `go` 关键字。

```go
package main

import (
    "fmt"
    "time"
)

func say(s string) {
    for i := 0; i < 3; i++ {
        time.Sleep(100 * time.Millisecond)
        fmt.Println(s)
    }
}

func main() {
    go say("world") // 启动一个新的 Goroutine
    say("hello")    // 当前 Goroutine 继续执行
}
```

### GMP 模型简介
Go 的调度器使用了 **GMP 模型**：
- **G (Goroutine)**: 协程，包含栈、指令指针等。
- **M (Machine)**: 内核级线程，负责执行代码。
- **P (Processor)**: 逻辑处理器，维护一个 Goroutine 队列，将 G 调度到 M 上运行。

这种 M:N 的调度模型使得成千上万个 Goroutine 可以复用少量的系统线程，极大地降低了上下文切换的开销。

## 2. Channel：不要通过共享内存来通信

Go 的并发哲学是："**不要通过共享内存来通信，而要通过通信来共享内存。**" Channel 就是这种通信机制的载体。

### 基本操作

```go
// 创建一个 channel (无缓冲)
ch := make(chan int)

// 发送数据
go func() {
    ch <- 42
}()

// 接收数据 (会阻塞直到收到数据)
v := <-ch
fmt.Println(v)
```

### 缓冲 Channel
带缓冲的 Channel 在缓冲区未满时发送不会阻塞。

```go
ch := make(chan int, 2)
ch <- 1
ch <- 2
// ch <- 3 // 此时会阻塞，因为缓冲区已满
```

### 关闭 Channel
```go
close(ch)
// 遍历 channel
for v := range ch {
    fmt.Println(v)
}
```

## 3. Select：多路复用

`select` 语句类似于 switch，但用于处理多个 channel 操作。它会阻塞直到其中一个 case 可以运行。

```go
func main() {
    c1 := make(chan string)
    c2 := make(chan string)

    go func() { time.Sleep(1 * time.Second); c1 <- "one" }()
    go func() { time.Sleep(2 * time.Second); c2 <- "two" }()

    for i := 0; i < 2; i++ {
        select {
        case msg1 := <-c1:
            fmt.Println("received", msg1)
        case msg2 := <-c2:
            fmt.Println("received", msg2)
        case <-time.After(3 * time.Second):
            fmt.Println("timeout")
        }
    }
}
```

## 4. Sync 包：同步原语

虽然推荐使用 Channel，但在某些场景（如保护共享状态）下，传统的锁机制依然很有用。

### Mutex (互斥锁)
```go
import "sync"

type SafeCounter struct {
    mu sync.Mutex
    v  map[string]int
}

func (c *SafeCounter) Inc(key string) {
    c.mu.Lock()
    defer c.mu.Unlock() // 确保释放锁
    c.v[key]++
}
```

### WaitGroup (等待组)
用于等待一组 Goroutine 完成。

```go
var wg sync.WaitGroup

for i := 0; i < 5; i++ {
    wg.Add(1) // 计数加 1
    go func(i int) {
        defer wg.Done() // 计数减 1
        fmt.Printf("Worker %d done\n", i)
    }(i)
}

wg.Wait() // 阻塞直到计数归零
fmt.Println("All workers done")
```

### Once (单例模式)
确保某个操作只执行一次（常用于单例初始化）。

```go
var once sync.Once

func setup() {
    fmt.Println("Init...")
}

func do() {
    once.Do(setup)
}
```

## 5. Context：上下文控制

`context` 包用于在 Goroutine 之间传递截止日期、取消信号和其他请求范围的值。它是处理超时和取消操作的标准方式。

```go
func worker(ctx context.Context) {
    for {
        select {
        case <-ctx.Done(): // 接收取消信号
            fmt.Println("Worker stopped")
            return
        default:
            fmt.Println("Working...")
            time.Sleep(500 * time.Millisecond)
        }
    }
}

func main() {
    // 创建一个带超时的 context
    ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
    defer cancel()

    go worker(ctx)

    <-ctx.Done() // 等待超时
    fmt.Println("Main finished")
}
```

## 总结

Go 的并发编程不仅强大而且易用。掌握以下原则：
1. 优先使用 **Channel** 进行通信。
2. 使用 **WaitGroup** 等待任务完成。
3. 使用 **Mutex** 保护共享数据。
4. 使用 **Context** 控制 Goroutine 的生命周期和超时。
5. 警惕 **Deadlock** (死锁) 和 **Race Condition** (竞态条件)，使用 `go run -race` 检测。
