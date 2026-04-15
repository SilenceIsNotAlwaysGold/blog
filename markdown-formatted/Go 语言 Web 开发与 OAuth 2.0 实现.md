---
title: "Go 语言 Web 开发与 OAuth 2.0 实现"
category: "编程语言-Golang"
board: "tech"
tags: ["Golang", "OAuth2", "Web开发", "JWT"]
summary: "Go 语言 Web 开发实战，涵盖 Gin 框架中间件设计、OAuth 2.0 鉴权流程与 JWT 令牌管理"
is_published: true
created_at: "2025-03-10T10:00:00Z"
updated_at: "2025-03-10T10:00:00Z"
---

# Go 语言 Web 开发与 OAuth 2.0 实现

在数据标注平台项目中，我用 Go 构建了后端 API 服务，集成了 OAuth 2.0 认证。Go 的强类型和高并发特性非常适合这类需要处理大量并发标注请求的场景。本文分享 Gin 框架的中间件设计和 OAuth 2.0 实现。

## 一、项目结构

```
annotation-platform/
├── cmd/
│   └── server/
│       └── main.go
├── internal/
│   ├── handler/          # 路由处理器
│   │   ├── auth.go
│   │   ├── task.go
│   │   └── annotation.go
│   ├── middleware/        # 中间件
│   │   ├── auth.go
│   │   ├── cors.go
│   │   ├── logger.go
│   │   └── ratelimit.go
│   ├── model/            # 数据模型
│   │   ├── user.go
│   │   └── task.go
│   ├── service/          # 业务逻辑
│   │   ├── auth.go
│   │   └── task.go
│   ├── repository/       # 数据库访问
│   │   ├── user.go
│   │   └── task.go
│   └── config/           # 配置
│       └── config.go
├── pkg/                  # 公共包
│   ├── jwt/
│   └── response/
├── go.mod
└── go.sum
```

## 二、Gin 框架核心实现

### 2.1 路由注册

```go
package main

import (
    "github.com/gin-gonic/gin"
    "annotation-platform/internal/handler"
    "annotation-platform/internal/middleware"
)

func setupRouter() *gin.Engine {
    r := gin.New()
    
    // 全局中间件
    r.Use(middleware.Logger())
    r.Use(middleware.Recovery())
    r.Use(middleware.CORS())
    r.Use(middleware.RequestID())
    
    // 公开接口
    public := r.Group("/api/v1")
    {
        public.POST("/auth/login", handler.Login)
        public.POST("/auth/register", handler.Register)
        public.GET("/auth/oauth/callback", handler.OAuthCallback)
        public.GET("/health", handler.HealthCheck)
    }
    
    // 需要认证的接口
    auth := r.Group("/api/v1")
    auth.Use(middleware.JWTAuth())
    {
        // 任务管理
        auth.GET("/tasks", handler.ListTasks)
        auth.POST("/tasks", middleware.RequireRole("admin", "manager"), handler.CreateTask)
        auth.GET("/tasks/:id", handler.GetTask)
        
        // 标注操作
        auth.POST("/tasks/:id/annotations", handler.CreateAnnotation)
        auth.PUT("/annotations/:id", handler.UpdateAnnotation)
        
        // 用户管理（仅管理员）
        admin := auth.Group("/admin")
        admin.Use(middleware.RequireRole("admin"))
        {
            admin.GET("/users", handler.ListUsers)
            admin.PUT("/users/:id/role", handler.UpdateUserRole)
        }
    }
    
    return r
}
```

### 2.2 中间件设计

**日志中间件**：

```go
package middleware

import (
    "time"
    "github.com/gin-gonic/gin"
    "go.uber.org/zap"
)

func Logger() gin.HandlerFunc {
    logger, _ := zap.NewProduction()
    
    return func(c *gin.Context) {
        start := time.Now()
        path := c.Request.URL.Path
        query := c.Request.URL.RawQuery
        requestID := c.GetHeader("X-Request-ID")
        
        // 处理请求
        c.Next()
        
        // 记录日志
        duration := time.Since(start)
        statusCode := c.Writer.Status()
        
        fields := []zap.Field{
            zap.String("request_id", requestID),
            zap.String("method", c.Request.Method),
            zap.String("path", path),
            zap.String("query", query),
            zap.Int("status", statusCode),
            zap.Duration("duration", duration),
            zap.String("client_ip", c.ClientIP()),
            zap.Int("body_size", c.Writer.Size()),
        }
        
        if statusCode >= 500 {
            logger.Error("Server error", fields...)
        } else if statusCode >= 400 {
            logger.Warn("Client error", fields...)
        } else if duration > 2*time.Second {
            logger.Warn("Slow request", fields...)
        } else {
            logger.Info("Request completed", fields...)
        }
    }
}
```

**限流中间件**：

```go
package middleware

import (
    "net/http"
    "sync"
    "time"
    "github.com/gin-gonic/gin"
    "golang.org/x/time/rate"
)

type IPRateLimiter struct {
    ips     map[string]*rate.Limiter
    mu      sync.RWMutex
    rate    rate.Limit
    burst   int
}

func NewIPRateLimiter(r rate.Limit, burst int) *IPRateLimiter {
    return &IPRateLimiter{
        ips:   make(map[string]*rate.Limiter),
        rate:  r,
        burst: burst,
    }
}

func (l *IPRateLimiter) GetLimiter(ip string) *rate.Limiter {
    l.mu.Lock()
    defer l.mu.Unlock()
    
    limiter, exists := l.ips[ip]
    if !exists {
        limiter = rate.NewLimiter(l.rate, l.burst)
        l.ips[ip] = limiter
    }
    return limiter
}

func RateLimit(rps float64, burst int) gin.HandlerFunc {
    limiter := NewIPRateLimiter(rate.Limit(rps), burst)
    
    // 定期清理过期 IP
    go func() {
        for range time.Tick(10 * time.Minute) {
            limiter.mu.Lock()
            limiter.ips = make(map[string]*rate.Limiter)
            limiter.mu.Unlock()
        }
    }()
    
    return func(c *gin.Context) {
        ip := c.ClientIP()
        if !limiter.GetLimiter(ip).Allow() {
            c.JSON(http.StatusTooManyRequests, gin.H{
                "error":       "rate limit exceeded",
                "retry_after": 1,
            })
            c.Abort()
            return
        }
        c.Next()
    }
}
```

## 三、OAuth 2.0 实现

### 3.1 OAuth 2.0 授权码流程

```
用户 → 前端 → 授权服务器（GitHub/Google）→ 回调 → 后端 → 颁发 JWT
```

```go
package handler

import (
    "context"
    "encoding/json"
    "net/http"
    "golang.org/x/oauth2"
    "golang.org/x/oauth2/github"
    "github.com/gin-gonic/gin"
)

var githubOAuth = &oauth2.Config{
    ClientID:     os.Getenv("GITHUB_CLIENT_ID"),
    ClientSecret: os.Getenv("GITHUB_CLIENT_SECRET"),
    RedirectURL:  "https://api.example.com/api/v1/auth/oauth/callback",
    Scopes:       []string{"user:email"},
    Endpoint:     github.Endpoint,
}

// OAuthLogin 生成授权 URL 并重定向
func OAuthLogin(c *gin.Context) {
    // 生成随机 state 防 CSRF
    state := generateRandomState()
    
    // 存储 state 到 Redis（5分钟过期）
    redisClient.Set(context.Background(), 
        "oauth_state:"+state, "1", 5*time.Minute)
    
    url := githubOAuth.AuthCodeURL(state, oauth2.AccessTypeOnline)
    c.Redirect(http.StatusTemporaryRedirect, url)
}

// OAuthCallback 处理授权回调
func OAuthCallback(c *gin.Context) {
    // 1. 验证 state
    state := c.Query("state")
    exists, _ := redisClient.Exists(context.Background(), "oauth_state:"+state).Result()
    if exists == 0 {
        c.JSON(http.StatusBadRequest, gin.H{"error": "invalid state"})
        return
    }
    redisClient.Del(context.Background(), "oauth_state:"+state)
    
    // 2. 用授权码换取 access token
    code := c.Query("code")
    token, err := githubOAuth.Exchange(context.Background(), code)
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "token exchange failed"})
        return
    }
    
    // 3. 用 access token 获取用户信息
    client := githubOAuth.Client(context.Background(), token)
    resp, err := client.Get("https://api.github.com/user")
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "failed to get user info"})
        return
    }
    defer resp.Body.Close()
    
    var githubUser struct {
        ID        int64  `json:"id"`
        Login     string `json:"login"`
        Email     string `json:"email"`
        AvatarURL string `json:"avatar_url"`
    }
    json.NewDecoder(resp.Body).Decode(&githubUser)
    
    // 4. 查找或创建用户
    user, err := userService.FindOrCreateByOAuth(context.Background(), &model.OAuthUser{
        Provider:   "github",
        ProviderID: fmt.Sprintf("%d", githubUser.ID),
        Username:   githubUser.Login,
        Email:      githubUser.Email,
        Avatar:     githubUser.AvatarURL,
    })
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "user creation failed"})
        return
    }
    
    // 5. 生成 JWT
    jwtToken, refreshToken, err := jwtService.GenerateTokenPair(user)
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "token generation failed"})
        return
    }
    
    // 6. 重定向到前端，带上 token
    redirectURL := fmt.Sprintf(
        "%s/auth/callback?token=%s&refresh_token=%s",
        os.Getenv("FRONTEND_URL"), jwtToken, refreshToken,
    )
    c.Redirect(http.StatusTemporaryRedirect, redirectURL)
}
```

### 3.2 JWT 令牌管理

```go
package jwt

import (
    "time"
    "errors"
    "github.com/golang-jwt/jwt/v5"
)

type Claims struct {
    UserID   uint   `json:"user_id"`
    Username string `json:"username"`
    Role     string `json:"role"`
    jwt.RegisteredClaims
}

type JWTService struct {
    secretKey       []byte
    accessTokenTTL  time.Duration
    refreshTokenTTL time.Duration
}

func NewJWTService(secret string) *JWTService {
    return &JWTService{
        secretKey:       []byte(secret),
        accessTokenTTL:  15 * time.Minute,
        refreshTokenTTL: 7 * 24 * time.Hour,
    }
}

func (s *JWTService) GenerateTokenPair(user *model.User) (string, string, error) {
    // Access Token
    accessClaims := &Claims{
        UserID:   user.ID,
        Username: user.Username,
        Role:     user.Role,
        RegisteredClaims: jwt.RegisteredClaims{
            ExpiresAt: jwt.NewNumericDate(time.Now().Add(s.accessTokenTTL)),
            IssuedAt:  jwt.NewNumericDate(time.Now()),
            Issuer:    "annotation-platform",
        },
    }
    accessToken := jwt.NewWithClaims(jwt.SigningMethodHS256, accessClaims)
    accessStr, err := accessToken.SignedString(s.secretKey)
    if err != nil {
        return "", "", err
    }
    
    // Refresh Token（有效期更长，但只包含最少信息）
    refreshClaims := &Claims{
        UserID: user.ID,
        RegisteredClaims: jwt.RegisteredClaims{
            ExpiresAt: jwt.NewNumericDate(time.Now().Add(s.refreshTokenTTL)),
            IssuedAt:  jwt.NewNumericDate(time.Now()),
        },
    }
    refreshToken := jwt.NewWithClaims(jwt.SigningMethodHS256, refreshClaims)
    refreshStr, err := refreshToken.SignedString(s.secretKey)
    if err != nil {
        return "", "", err
    }
    
    return accessStr, refreshStr, nil
}

func (s *JWTService) ValidateToken(tokenStr string) (*Claims, error) {
    token, err := jwt.ParseWithClaims(tokenStr, &Claims{}, func(token *jwt.Token) (interface{}, error) {
        if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
            return nil, errors.New("unexpected signing method")
        }
        return s.secretKey, nil
    })
    
    if err != nil {
        return nil, err
    }
    
    claims, ok := token.Claims.(*Claims)
    if !ok || !token.Valid {
        return nil, errors.New("invalid token")
    }
    
    return claims, nil
}
```

### 3.3 认证中间件

```go
package middleware

func JWTAuth() gin.HandlerFunc {
    return func(c *gin.Context) {
        authHeader := c.GetHeader("Authorization")
        if authHeader == "" {
            c.JSON(http.StatusUnauthorized, gin.H{"error": "missing authorization header"})
            c.Abort()
            return
        }
        
        // Bearer token
        parts := strings.SplitN(authHeader, " ", 2)
        if len(parts) != 2 || parts[0] != "Bearer" {
            c.JSON(http.StatusUnauthorized, gin.H{"error": "invalid authorization format"})
            c.Abort()
            return
        }
        
        claims, err := jwtService.ValidateToken(parts[1])
        if err != nil {
            c.JSON(http.StatusUnauthorized, gin.H{"error": "invalid token"})
            c.Abort()
            return
        }
        
        // 检查 token 是否被主动吊销（黑名单）
        revoked, _ := redisClient.Exists(c, "token_blacklist:"+parts[1]).Result()
        if revoked > 0 {
            c.JSON(http.StatusUnauthorized, gin.H{"error": "token revoked"})
            c.Abort()
            return
        }
        
        // 存入上下文
        c.Set("user_id", claims.UserID)
        c.Set("username", claims.Username)
        c.Set("role", claims.Role)
        
        c.Next()
    }
}

func RequireRole(roles ...string) gin.HandlerFunc {
    return func(c *gin.Context) {
        userRole, exists := c.Get("role")
        if !exists {
            c.JSON(http.StatusForbidden, gin.H{"error": "no role information"})
            c.Abort()
            return
        }
        
        for _, role := range roles {
            if userRole.(string) == role {
                c.Next()
                return
            }
        }
        
        c.JSON(http.StatusForbidden, gin.H{"error": "insufficient permissions"})
        c.Abort()
    }
}
```

## 四、Token 刷新与吊销

```go
// Token 刷新接口
func RefreshToken(c *gin.Context) {
    var req struct {
        RefreshToken string `json:"refresh_token" binding:"required"`
    }
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "refresh_token required"})
        return
    }
    
    claims, err := jwtService.ValidateToken(req.RefreshToken)
    if err != nil {
        c.JSON(http.StatusUnauthorized, gin.H{"error": "invalid refresh token"})
        return
    }
    
    // 获取用户最新信息
    user, err := userRepo.GetByID(c, claims.UserID)
    if err != nil || !user.IsActive {
        c.JSON(http.StatusUnauthorized, gin.H{"error": "user not found or disabled"})
        return
    }
    
    // 生成新的 token 对
    accessToken, refreshToken, err := jwtService.GenerateTokenPair(user)
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "token generation failed"})
        return
    }
    
    // 将旧 refresh token 加入黑名单
    ttl := time.Until(claims.ExpiresAt.Time)
    redisClient.Set(c, "token_blacklist:"+req.RefreshToken, "1", ttl)
    
    c.JSON(http.StatusOK, gin.H{
        "access_token":  accessToken,
        "refresh_token": refreshToken,
    })
}
```

## 总结

Go Web 开发与 OAuth 2.0 的要点：

1. **项目结构**：按职责分层（handler → service → repository），保持清晰
2. **中间件链**：Logger → Recovery → CORS → RateLimit → Auth，顺序很重要
3. **OAuth 2.0**：state 参数防 CSRF，授权码只能使用一次
4. **JWT 双 Token**：短期 access token + 长期 refresh token，平衡安全和体验
5. **Token 吊销**：用 Redis 黑名单实现，TTL 与 token 过期时间一致
6. **Go 的优势**：强类型减少运行时错误，goroutine 天然支持高并发
