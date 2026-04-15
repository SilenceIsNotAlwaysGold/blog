---
title: "Shell 脚本编程从入门到精通"
summary: "系统学习 Shell 脚本编程，从变量、流程控制到函数与数组，结合自动化备份和日志清理等实战案例，提升你的运维自动化效率。"
board: "tech"
category: "Linux系统"
tags:
  - "Linux"
  - "Shell"
  - "脚本"
  - "自动化"
cover_image: ""
author: "博主"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---

# Shell 脚本编程从入门到精通

Shell 脚本是 Linux 运维自动化的基石。通过编写脚本，我们可以将重复性的任务自动化，减少人为错误。本文将带你从零开始编写高效的 Shell 脚本。

## 1. 脚本基础

### Hello World
创建一个文件 `hello.sh`：

```bash
#!/bin/bash
# 第一行指定解释器

echo "Hello, World!"
```

执行脚本：
```bash
chmod +x hello.sh
./hello.sh
```

### 变量
```bash
#!/bin/bash

# 定义变量（等号两边不能有空格）
NAME="Clouditera"
echo "Hello, $NAME"
echo "Hello, ${NAME}" # 推荐使用花括号

# 只读变量
readonly URL="http://google.com"

# 删除变量
unset NAME
```

## 2. 传递参数

脚本可以在执行时接收参数。

```bash
#!/bin/bash
# run: ./script.sh param1 param2

echo "文件名: $0"
echo "第一个参数: $1"
echo "第二个参数: $2"
echo "参数个数: $#"
echo "所有参数: $*"
echo "最后运行命令的退出状态: $?" # 0 表示成功，非 0 表示失败
```

## 3. 运算符与条件判断

### 算术运算
```bash
a=10
b=20

# 使用 expr (注意空格和反引号)
val=`expr $a + $b`

# 使用 $(( )) (推荐)
val=$(($a + $b))
echo "Sum: $val"
```

### 条件判断 (if)
注意 `[` 和 `]` 内部必须有空格。

```bash
#!/bin/bash

SCORE=85

if [ $SCORE -ge 90 ]; then
    echo "优秀"
elif [ $SCORE -ge 60 ]; then
    echo "及格"
else
    echo "不及格"
fi
```

常用比较符：
- `-eq`: 等于 (equal)
- `-ne`: 不等于 (not equal)
- `-gt`: 大于 (greater than)
- `-lt`: 小于 (less than)
- `-z`: 字符串长度为 0
- `-f`: 文件存在且是普通文件
- `-d`: 目录存在

## 4. 流程控制

### for 循环
```bash
# 遍历列表
for loop in 1 2 3 4 5
do
    echo "The value is: $loop"
done

# 遍历文件
for file in *.txt
do
    echo "Found text file: $file"
done
```

### while 循环
```bash
int=1
while(( $int<=5 ))
do
    echo $int
    let "int++"
done
```

## 5. 函数

```bash
#!/bin/bash

function sayHello(){
    echo "Hello, $1!"
    return 0
}

# 调用函数
sayHello "World"
```

## 6. 实战案例

### 案例一：数据库每日备份

```bash
#!/bin/bash

# 配置
DB_USER="root"
DB_PASS="password"
DB_NAME="mydb"
BACKUP_DIR="/data/backup"
DATE=$(date +%Y%m%d_%H%M%S)

# 创建目录
mkdir -p $BACKUP_DIR

# 备份
echo "Starting backup for $DB_NAME..."
mysqldump -u$DB_USER -p$DB_PASS $DB_NAME > $BACKUP_DIR/$DB_NAME_$DATE.sql

# 检查结果
if [ $? -eq 0 ]; then
    echo "Backup successful: $BACKUP_DIR/$DB_NAME_$DATE.sql"
    # 压缩
    gzip $BACKUP_DIR/$DB_NAME_$DATE.sql
else
    echo "Backup failed!"
    exit 1
fi

# 删除 7 天前的备份
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -exec rm -f {} \;
echo "Old backups cleaned."
```

### 案例二：服务器资源监控报警

```bash
#!/bin/bash

# 获取 CPU 使用率
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}')
CPU_INT=$(printf "%.0f" $CPU_USAGE)

# 阈值
THRESHOLD=80

if [ $CPU_INT -gt $THRESHOLD ]; then
    echo "Warning: CPU usage is high: $CPU_USAGE%" | mail -s "Server Alert" admin@example.com
fi
```

## 7. 调试技巧

- `bash -x script.sh`: 执行脚本并显示每一行命令，非常适合排错。
- `bash -n script.sh`: 检查语法错误但不执行。
- 在脚本中添加 `set -e`: 遇到错误立即退出。
- 在脚本中添加 `set -x`: 开启调试模式。

## 总结

Shell 脚本并不复杂，关键在于多写多练。通过将日常的命令组合成脚本，你可以极大地解放双手，提高工作效率。
