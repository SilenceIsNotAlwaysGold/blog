---
title: "Golang网络编程、数据库编程和Web框架"
summary: "网络编程 HTTP服务器开发（net/http包） RESTful API开发 数据库编程 连接和操作数据库（使用database/sql包） 使用gorm ORM框架 **安装gorm**： **代码示例**： Web框架 使用Gin框架 **安装Gin**： **代码示例**： 使用Echo框架 **安装Echo**： **代码示例**："
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

### 网络编程
#### HTTP服务器开发（net/http包）
```go
package main

import (
    "fmt"
    "net/http"
)

func helloHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Hello, World!")
}

func main() {
    http.HandleFunc("/", helloHandler)
    fmt.Println("Starting server at port 8080")
    if err := http.ListenAndServe(":8080", nil); err != nil {
        fmt.Println("Error starting server:", err)
    }
}
```

#### RESTful API开发
```go
package main

import (
    "encoding/json"
    "net/http"
)

type Response struct {
    Message string `json:"message"`
}

func apiHandler(w http.ResponseWriter, r *http.Request) {
    response := Response{Message: "Hello, API!"}
    json.NewEncoder(w).Encode(response)
}

func main() {
    http.HandleFunc("/api", apiHandler)
    http.ListenAndServe(":8080", nil)
}
```

### 数据库编程
#### 连接和操作数据库（使用database/sql包）
```go
package main

import (
    "database/sql"
    "fmt"
    _ "github.com/go-sql-driver/mysql"
)

func main() {
    db, err := sql.Open("mysql", "user:password@tcp(127.0.0.1:3306)/testdb")
    if err != nil {
        fmt.Println("Error connecting to the database:", err)
        return
    }
    defer db.Close()

    var name string
    err = db.QueryRow("SELECT name FROM users WHERE id = ?", 1).Scan(&name)
    if err != nil {
        fmt.Println("Error querying the database:", err)
        return
    }
    fmt.Println("User name:", name)
}
```

#### 使用gorm ORM框架
1. **安装gorm**：

```shell
go get -u gorm.io/gorm
go get -u gorm.io/driver/mysql
```

2. **代码示例**：

```go
package main

import (
    "fmt"
    "gorm.io/driver/mysql"
    "gorm.io/gorm"
)

type User struct {
    ID   uint
    Name string
}

func main() {
    dsn := "user:password@tcp(127.0.0.1:3306)/testdb?charset=utf8mb4&parseTime=True&loc=Local"
    db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
    if err != nil {
        fmt.Println("Error connecting to the database:", err)
        return
    }

    db.AutoMigrate(&User{})

    db.Create(&User{Name: "John Doe"})

    var user User
    db.First(&user, 1)
    fmt.Println("User name:", user.Name)
}
```

### Web框架
#### 使用Gin框架
1. **安装Gin**：

```shell
go get -u github.com/gin-gonic/gin
```

2. **代码示例**：

```go
package main

import (
    "github.com/gin-gonic/gin"
)

func main() {
    router := gin.Default()
    router.GET("/", func(c *gin.Context) {
        c.JSON(200, gin.H{
            "message": "Hello, World!",
        })
    })
    router.Run(":8080")
}
```

#### 使用Echo框架
1. **安装Echo**：

```shell
go get -u github.com/labstack/echo/v4
```

2. **代码示例**：

```go
package main

import (
    "github.com/labstack/echo/v4"
    "net/http"
)

func main() {
    e := echo.New()
    e.GET("/", func(c echo.Context) error {
        return c.JSON(http.StatusOK, map[string]string{
            "message": "Hello, World!",
        })
    })
    e.Start(":8080")
}
```
