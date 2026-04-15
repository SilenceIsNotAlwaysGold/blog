---
title: "Golang的数据库连接"
summary: "基础概念 Golang通过`database/sql`包提供了一套通用的数据库接口，这个包支持多种数据库，包括SQLite、MySQL、PostgreSQL等。具体的数据库操作是通过数据库驱动来实现的，例如： `github.com/mattn/go-sqlite3` 用于SQLite `github."
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

### 1. 基础概念
Golang通过`database/sql`包提供了一套通用的数据库接口，这个包支持多种数据库，包括SQLite、MySQL、PostgreSQL等。具体的数据库操作是通过数据库驱动来实现的，例如：

+ `github.com/mattn/go-sqlite3` 用于SQLite
+ `github.com/go-sql-driver/mysql` 用于MySQL
+ `github.com/lib/pq` 用于PostgreSQL

### 2. 使用步骤
#### 1. 安装数据库驱动
首先，你需要安装相应的数据库驱动。例如，使用SQLite时：

```shell
go get github.com/mattn/go-sqlite3
```

#### 2. 导入必要的包
在代码中导入`database/sql`包和相应的数据库驱动。

```go
import (
    "database/sql"
    _ "github.com/mattn/go-sqlite3"
    "fmt"
    "log"
)
```

#### 3. 打开数据库连接
使用`sql.Open`函数打开数据库连接。`sql.Open`需要两个参数：驱动名称和数据源名称。

```go
db, err := sql.Open("sqlite3", "./test.db")
if err != nil {
    log.Fatal(err)
}
defer db.Close()
```

#### 4. 验证数据库连接
使用`db.Ping`方法验证数据库连接是否成功。

```go
if err := db.Ping(); err != nil {
    log.Fatal(err)
}
```

#### 5. 创建表
使用`db.Exec`方法执行SQL语句来创建表。

```go
createTableSQL := `CREATE TABLE IF NOT EXISTS users (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" TEXT,
    "age" INTEGER
);`
_, err = db.Exec(createTableSQL)
if err != nil {
    log.Fatal(err)
}
```

#### 6. 增删改查操作
##### 增加数据
使用`db.Exec`方法插入数据。

```go
insertUserSQL := `INSERT INTO users (name, age) VALUES (?, ?)`
_, err = db.Exec(insertUserSQL, "Alice", 30)
if err != nil {
    log.Fatal(err)
}
```

##### 查询数据
使用`db.Query`或`db.QueryRow`方法查询数据。

```go
queryUserSQL := `SELECT id, name, age FROM users WHERE name = ?`
row := db.QueryRow(queryUserSQL, "Alice")

var id int
var name string
var age int
err = row.Scan(&id, &name, &age)
if err != nil {
    log.Fatal(err)
}
fmt.Printf("User: ID=%d, Name=%s, Age=%d\n", id, name, age)
```

##### 更新数据
使用`db.Exec`方法更新数据。

```go
updateUserSQL := `UPDATE users SET age = ? WHERE name = ?`
_, err = db.Exec(updateUserSQL, 31, "Alice")
if err != nil {
    log.Fatal(err)
}
```

##### 删除数据
使用`db.Exec`方法删除数据。

```go
deleteUserSQL := `DELETE FROM users WHERE name = ?`
_, err = db.Exec(deleteUserSQL, "Alice")
if err != nil {
    log.Fatal(err)
}
```

### 3. 完整示例
下面是一个完整的示例，演示如何使用Golang与SQLite进行数据库连接和基本的CRUD操作。

```go
package main

import (
    "database/sql"
    "fmt"
    "log"
    _ "github.com/mattn/go-sqlite3"
)

type User struct {
    ID   int
    Name string
    Age  int
}

func main() {
    db, err := sql.Open("sqlite3", "./test.db")
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    if err := db.Ping(); err != nil {
        log.Fatal(err)
    }

    createTableSQL := `CREATE TABLE IF NOT EXISTS users (
        "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "name" TEXT,
        "age" INTEGER
    );`
    _, err = db.Exec(createTableSQL)
    if err != nil {
        log.Fatal(err)
    }

    addUser(db, "Alice", 30)
    addUser(db, "Bob", 25)

    users, err := getUsers(db)
    if err != nil {
        log.Fatal(err)
    }
    for _, user := range users {
        fmt.Printf("User: ID=%d, Name=%s, Age=%d\n", user.ID, user.Name, user.Age)
    }

    updateUser(db, 1, "Alice", 31)
    deleteUser(db, 2)
}

func addUser(db *sql.DB, name string, age int) {
    insertUserSQL := `INSERT INTO users (name, age) VALUES (?, ?)`
    _, err := db.Exec(insertUserSQL, name, age)
    if err != nil {
        log.Fatal(err)
    }
}

func getUsers(db *sql.DB) ([]User, error) {
    queryUserSQL := `SELECT id, name, age FROM users`
    rows, err := db.Query(queryUserSQL)
    if err != nil {
        return nil, err
    }
    defer rows.Close()

    var users []User
    for rows.Next() {
        var user User
        err = rows.Scan(&user.ID, &user.Name, &user.Age)
        if err != nil {
            return nil, err
        }
        users = append(users, user)
    }

    return users, nil
}

func updateUser(db *sql.DB, id int, name string, age int) {
    updateUserSQL := `UPDATE users SET name = ?, age = ? WHERE id = ?`
    _, err := db.Exec(updateUserSQL, name, age, id)
    if err != nil {
        log.Fatal(err)
    }
}

func deleteUser(db *sql.DB, id int) {
    deleteUserSQL := `DELETE FROM users WHERE id = ?`
    _, err := db.Exec(deleteUserSQL, id)
    if err != nil {
        log.Fatal(err)
    }
}
```

这个示例展示了如何在Golang中使用SQLite进行数据库连接和基本的增删改查操作。你可以根据实际需要修改代码，并使用其他数据库驱动实现类似的功能。
