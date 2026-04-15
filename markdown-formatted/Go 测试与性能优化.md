---
title: "Go 测试与性能优化"
summary: "掌握 Go 语言内置的 testing 框架，编写单元测试、基准测试（Benchmark）和示例代码，结合 pprof 工具进行 CPU 和内存性能分析与调优。"
board: "tech"
category: "编程语言-Golang"
tags:
  - "Go"
  - "Golang"
  - "测试"
  - "性能优化"
cover_image: ""
author: "博主"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---

# Go 测试与性能优化

Go 语言自带了强大的测试工具链，无需第三方库即可完成单元测试、基准测试和性能分析。本文将介绍如何编写高质量的测试代码，并利用 `pprof` 进行性能调优。

## 1. 单元测试 (Unit Test)

Go 的测试文件以 `_test.go` 结尾，测试函数必须以 `Test` 开头。

### 示例代码 (calc.go)
```go
package calc

func Add(a, b int) int {
    return a + b
}
```

### 测试代码 (calc_test.go)
```go
package calc

import "testing"

func TestAdd(t *testing.T) {
    got := Add(2, 3)
    want := 5

    if got != want {
        t.Errorf("Add(2, 3) = %d; want %d", got, want)
    }
}
```

### 表格驱动测试 (Table Driven Tests)
Go 社区推荐的测试模式，易于扩展。

```go
func TestAddMultiple(t *testing.T) {
    cases := []struct {
        name string
        a, b int
        want int
    }{
        {"positive", 1, 2, 3},
        {"negative", -1, -2, -3},
        {"mixed", -1, 1, 0},
    }

    for _, tc := range cases {
        t.Run(tc.name, func(t *testing.T) {
            got := Add(tc.a, tc.b)
            if got != tc.want {
                t.Errorf("Add(%d, %d) = %d; want %d", tc.a, tc.b, got, tc.want)
            }
        })
    }
}
```

运行测试：
```bash
go test -v .
```

## 2. 基准测试 (Benchmark)

基准测试用于衡量代码性能，函数以 `Benchmark` 开头。

```go
func BenchmarkAdd(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Add(1, 2)
    }
}
```

运行基准测试：
```bash
# -bench=. 运行所有基准测试
# -benchmem 显示内存分配情况
go test -bench=. -benchmem
```

输出示例：
```bash
BenchmarkAdd-8   1000000000   0.315 ns/op   0 B/op   0 allocs/op
```

## 3. 示例代码 (Example)

示例代码既是文档，也是测试。函数以 `Example` 开头。

```go
func ExampleAdd() {
    sum := Add(1, 5)
    fmt.Println(sum)
    // Output: 6
}
```

`go test` 会自动检查 Output 注释是否匹配实际输出。

## 4. 性能分析 (Profiling)

当程序性能不达标时，盲目猜测是无效的。Go 提供了 `pprof` 工具进行采样分析。

### 启用 pprof

对于 Web 服务，只需引入 `net/http/pprof`：

```go
import _ "net/http/pprof"

func main() {
    // 启动 pprof server
    go func() {
        log.Println(http.ListenAndServe("localhost:6060", nil))
    }()

    // ... 业务代码
}
```

### 收集数据

访问 `http://localhost:6060/debug/pprof/` 可以看到概览。

使用 `go tool pprof` 命令行工具进行交互式分析：

```bash
# 分析 CPU (采样 30 秒)
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30

# 分析 Heap 内存
go tool pprof http://localhost:6060/debug/pprof/heap
```

### 分析命令
进入 pprof 交互模式后：
- `top`: 显示消耗资源最多的函数。
- `list FunctionName`: 查看特定函数的代码耗时。
- `web`: 在浏览器中生成火焰图或调用图（需安装 Graphviz）。

## 5. 常见优化技巧

### 1. 预分配切片 (Pre-allocate Slices)
避免切片在 append 时频繁扩容。

```go
// Bad
data := make([]int, 0)

// Good (如果我们知道大概数量)
data := make([]int, 0, 1000)
```

### 2. 字符串拼接
在循环中拼接字符串，使用 `strings.Builder` 代替 `+`。

```go
var b strings.Builder
for i := 0; i < 1000; i++ {
    b.WriteString("test")
}
return b.String()
```

### 3. 复用对象 (sync.Pool)
对于频繁创建和销毁的大对象，使用对象池减少 GC 压力。

```go
var bufPool = sync.Pool{
    New: func() interface{} {
        return new(bytes.Buffer)
    },
}

// Get & Put
buf := bufPool.Get().(*bytes.Buffer)
buf.Reset()
defer bufPool.Put(buf)
```

## 总结

- **测试**是代码质量的保证，学会写 Table Driven Tests。
- **基准测试**帮助我们量化性能。
- **pprof** 帮助我们定位瓶颈（CPU 热点或内存分配）。
- 优化应基于数据，而非直觉。
