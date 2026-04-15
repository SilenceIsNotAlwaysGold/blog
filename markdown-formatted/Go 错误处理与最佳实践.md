---
title: "Go 错误处理与最佳实践"
summary: "探讨 Go 语言独特的错误处理机制，介绍 error 接口、Panic 与 Recover，以及 Go 1.13+ 的错误包装与 Unwrap，分享生产环境中的错误处理最佳实践。"
board: "tech"
category: "编程语言-Golang"
tags:
  - "Go"
  - "Golang"
  - "错误处理"
  - "最佳实践"
cover_image: ""
author: "博主"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---

# Go 错误处理与最佳实践

Go 语言对待错误的方式与 Java 或 Python 的 `try-catch` 机制截然不同。Go 将错误视为值（Values），通过返回值显式传递。这种设计虽然显得有些啰嗦（著名的 `if err != nil`），但能让控制流更加清晰。

## 1. 基础错误处理

### Error 接口
Go 中的错误是一个实现了 `error` 接口的值：

```go
type error interface {
    Error() string
}
```

### 创建错误
```go
import "errors"
import "fmt"

// 简单错误
var ErrNotFound = errors.New("record not found")

// 格式化错误
func divide(a, b int) (int, error) {
    if b == 0 {
        return 0, fmt.Errorf("cannot divide %d by zero", a)
    }
    return a / b, nil
}
```

### 检查错误
```go
result, err := divide(10, 0)
if err != nil {
    // 处理错误
    fmt.Println("Error:", err)
    return
}
```

## 2. 错误包装 (Error Wrapping)

在 Go 1.13 之前，我们通常会丢失原始错误的类型信息。Go 1.13 引入了 `%w` 动词来包装错误。

```go
func openFile(filename string) error {
    if _, err := os.Open(filename); err != nil {
        // 包装错误，保留原始错误信息
        return fmt.Errorf("failed to open file %s: %w", filename, err)
    }
    return nil
}
```

## 3. 错误判断 (Is & As)

### errors.Is
用于判断错误链中是否包含特定错误（替代 `==`）。

```go
err := openFile("test.txt")
if errors.Is(err, os.ErrNotExist) {
    fmt.Println("File does not exist")
}
```

### errors.As
用于将错误转换为特定类型（替代类型断言）。

```go
var pathError *os.PathError
if errors.As(err, &pathError) {
    fmt.Println("Failed at path:", pathError.Path)
}
```

## 4. Panic 与 Recover

`panic` 用于不可恢复的严重错误（如数组越界）。在业务代码中应尽量避免使用 `panic`，而是返回 error。

`recover` 可以捕获 `panic`，防止程序崩溃。通常在 `defer` 中使用。

```go
func safeHandler() {
    defer func() {
        if r := recover(); r != nil {
            fmt.Println("Recovered from panic:", r)
        }
    }()

    // 可能会 panic 的代码
    var slice []int
    fmt.Println(slice[0])
}
```

> **最佳实践**：不要跨包 panic。库函数应该返回 error，只有 main 函数或顶层处理逻辑才决定是否 panic。

## 5. 最佳实践总结

### 1. 哨兵错误 (Sentinel Errors)
预定义特定的错误变量，方便外部检查。

```go
var (
    ErrInvalidInput = errors.New("invalid input")
    ErrDatabase     = errors.New("database error")
)
```

### 2. 自定义错误类型
当需要携带更多上下文信息时，使用结构体实现 `error` 接口。

```go
type RequestError struct {
    StatusCode int
    Err        error
}

func (r *RequestError) Error() string {
    return fmt.Sprintf("status %d: %v", r.StatusCode, r.Err)
}
```

### 3. 只处理一次错误
不要记录日志后又返回错误，这会导致日志重复。

**反例**：
```go
if err != nil {
    log.Println(err) // 记录一次
    return err       // 上层可能又记录一次
}
```

**正例**：
要么处理降级，要么包装后返回，交给顶层统一记录日志。

```go
if err != nil {
    return fmt.Errorf("operation failed: %w", err)
}
```

### 4. 善用 defer 关闭资源
无论是否发生错误，确保资源被释放。

```go
f, err := os.Open("file.txt")
if err != nil {
    return err
}
defer f.Close()
// ... read file
```

## 结语
Go 的错误处理哲学强调显式和可控。虽然代码量稍多，但它强制开发者思考每一步可能出现的异常，从而构建出更加健壮的软件系统。
