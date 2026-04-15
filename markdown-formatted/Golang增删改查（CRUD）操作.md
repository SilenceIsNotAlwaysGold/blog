---
title: "Golang增删改查（CRUD）操作"
summary: "学习规划 **理解基础知识** 学习Golang的基本语法和结构 熟悉SQL的基础语法，包括SELECT、INSERT、UPDATE和DELETE **设置开发环境** 安装Go编译器和设置GOPATH 安装SQLite和MySQL数据库 安装相应的数据库驱动 **SQLite CRUD操作** 创建SQLite数据库 使用Golang连接SQLite 实现..."
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

### 学习规划
1. **理解基础知识**
    - 学习Golang的基本语法和结构
    - 熟悉SQL的基础语法，包括SELECT、INSERT、UPDATE和DELETE
1. **设置开发环境**
    - 安装Go编译器和设置GOPATH
    - 安装SQLite和MySQL数据库
    - 安装相应的数据库驱动
1. **SQLite CRUD操作**
    - 创建SQLite数据库
    - 使用Golang连接SQLite
    - 实现基本的增删改查操作
1. **MySQL CRUD操作**
    - 创建MySQL数据库
    - 使用Golang连接MySQL
    - 实现基本的增删改查操作
1. **构建一个简单的Web应用**
    - 使用Golang的`net/http`包创建简单的Web服务器
    - 使用Golang的Web框架（例如Gin、Echo）构建RESTful API，实现CRUD操作

### 代码实例
#### 1. SQLite CRUD操作
**步骤：**

1. 安装SQLite驱动

```shell
go get github.com/mattn/go-sqlite3
```

1. 创建项目文件结构

```plain
my-go-project/
├── main.go
└── database/
    └── database.go
```

1. 编写代码

`database/database.go`** 文件内容**

```go
package database

import (
    "database/sql"
    _ "github.com/mattn/go-sqlite3" // SQLite驱动
    "log"
)

// DB是全局的数据库连接实例
var DB *sql.DB

// InitDB 初始化数据库并创建表
func InitDB(filepath string) error {
    var err error
    // 打开数据库连接
    DB, err = sql.Open("sqlite3", filepath)
    if err != nil {
        return err
    }

    // 验证数据库连接
    if err = DB.Ping(); err != nil {
        return err
    }

    // 创建表
    return createTable()
}

// createTable 创建用户表
func createTable() error {
    createTableSQL := `CREATE TABLE IF NOT EXISTS users (
        "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "name" TEXT,
        "age" INTEGER
    );`
    _, err := DB.Exec(createTableSQL)
    if err != nil {
        log.Println("Error creating table:", err)
    }
    return err
}
```

`main.go`** 文件内容**

```go
package main

import (
    "database/sql"
    "fmt"
    "log"
    "my-go-project/database" // 导入本地数据库包
)

// User 定义用户结构
type User struct {
    ID   int
    Name string
    Age  int
}

func main() {
    // 初始化数据库
    err := database.InitDB("./test.db")
    if err != nil {
        log.Fatal(err)
    }

    // 增加数据
    addUser("Alice", 30)
    addUser("Bob", 25)

    // 查询数据
    users, err := getUsers()
    if err != nil {
        log.Fatal(err)
    }
    for _, user := range users {
        fmt.Printf("User: ID=%d, Name=%s, Age=%d\n", user.ID, user.Name, user.Age)
    }

    // 更新数据
    updateUser(1, "Alice", 31)

    // 删除数据
    deleteUser(2)
}

// addUser 增加用户
func addUser(name string, age int) {
    // 准备插入SQL语句
    insertUserSQL := `INSERT INTO users (name, age) VALUES (?, ?)`
    _, err := database.DB.Exec(insertUserSQL, name, age)
    if err != nil {
        log.Fatal(err)
    }
}

// getUsers 获取所有用户
func getUsers() ([]User, error) {
    // 准备查询SQL语句
    queryUserSQL := `SELECT id, name, age FROM users`
    rows, err := database.DB.Query(queryUserSQL)
    if err != nil {
        return nil, err
    }
    defer rows.Close() // 确保查询完毕后关闭结果集

    var users []User
    for rows.Next() {
        var user User
        // 扫描结果集中的每一行
        err = rows.Scan(&user.ID, &user.Name, &user.Age)
        if err != nil {
            return nil, err
        }
        users = append(users, user)
    }

    return users, nil
}

// updateUser 更新用户信息
func updateUser(id int, name string, age int) {
    // 准备更新SQL语句
    updateUserSQL := `UPDATE users SET name = ?, age = ? WHERE id = ?`
    _, err := database.DB.Exec(updateUserSQL, name, age, id)
    if err != nil {
        log.Fatal(err)
    }
}

// deleteUser 删除用户
func deleteUser(id int) {
    // 准备删除SQL语句
    deleteUserSQL := `DELETE FROM users WHERE id = ?`
    _, err := database.DB.Exec(deleteUserSQL, id)
    if err != nil {
        log.Fatal(err)
    }
}
```

#### 2. MySQL CRUD操作
**步骤：**

1. 安装MySQL驱动

```shell
go get github.com/go-sql-driver/mysql
```

1. 创建项目文件结构

```plain
my-go-project/
├── main.go
└── database/
    └── database.go
```

1. 编写代码

`database/database.go`** 文件内容**

```go
package database

import (
    "database/sql"
    _ "github.com/go-sql-driver/mysql" // MySQL驱动
    "log"
)

// DB是全局的数据库连接实例
var DB *sql.DB

// InitDB 初始化数据库并创建表
func InitDB(dsn string) error {
    var err error
    // 打开数据库连接
    DB, err = sql.Open("mysql", dsn)
    if err != nil {
        return err
    }

    // 验证数据库连接
    if err = DB.Ping(); err != nil {
        return err
    }

    // 创建表
    return createTable()
}

// createTable 创建用户表
func createTable() error {
    createTableSQL := `CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT,
        name VARCHAR(50),
        age INT,
        PRIMARY KEY (id)
    );`
    _, err := DB.Exec(createTableSQL)
    if err != nil {
        log.Println("Error creating table:", err)
    }
    return err
}
```

`main.go`** 文件内容**

```go
package main

import (
    "database/sql"
    "fmt"
    "log"
    "my-go-project/database" // 导入本地数据库包
)

// User 定义用户结构
type User struct {
    ID   int
    Name string
    Age  int
}

func main() {
    // 初始化数据库
    dsn := "user:password@tcp(127.0.0.1:3306)/testdb"
    err := database.InitDB(dsn)
    if err != nil {
        log.Fatal(err)
    }

    // 增加数据
    addUser("Alice", 30)
    addUser("Bob", 25)

    // 查询数据
    users, err := getUsers()
    if err != nil {
        log.Fatal(err)
    }
    for _, user := range users {
        fmt.Printf("User: ID=%d, Name=%s, Age=%d\n", user.ID, user.Name, user.Age)
    }

    // 更新数据
    updateUser(1, "Alice", 31)

    // 删除数据
    deleteUser(2)
}

// addUser 增加用户
func addUser(name string, age int) {
    // 准备插入SQL语句
    insertUserSQL := `INSERT INTO users (name, age) VALUES (?, ?)`
    _, err := database.DB.Exec(insertUserSQL, name, age)
    if err != nil {
        log.Fatal(err)
    }
}

// getUsers 获取所有用户
func getUsers() ([]User, error) {
    // 准备查询SQL语句
    queryUserSQL := `SELECT id, name, age FROM users`
    rows, err := database.DB.Query(queryUserSQL)
    if err != nil {
        return nil, err
    }
    defer rows.Close() // 确保查询完毕后关闭结果集

    var users []User
    for rows.Next() {
        var user User
        // 扫描结果集中的每一行
        err = rows.Scan(&user.ID, &user.Name, &user.Age)
        if err != nil {
            return nil, err
        }
        users = append(users, user)
    }

    return users, nil
}

// updateUser 更新用户信息
func updateUser(id int, name string, age int) {
    // 准备更新SQL语句
    updateUserSQL := `UPDATE users SET name = ?, age = ? WHERE id = ?`
    _, err := database.DB.Exec(updateUserSQL, name, age, id)
    if err != nil {
        log
```
