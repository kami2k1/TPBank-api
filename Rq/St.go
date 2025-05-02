package Rq

import (
	"net/http"
	"time"
)

// Session
type Session struct {
	Client  *http.Client
	Headers map[string]string
}

func NewSession() *Session {
	return &Session{
		Client: &http.Client{
			Timeout: time.Second * 10,
		},
		Headers: map[string]string{
			"User-Agent":       "Mozilla/5.0 (X11; Linux x86_64) Chrome/136.0.0.0",
			"Content-Type":     "application/json",
			"device_id":        "J4AEald6hatSqk5b6Leqlk1iBVUuYWHpJGBvjsQD0yypQ",
			"platform_name":    "WEB",
			"platform_version": "136",
			"app_version":      "2025.03.31",
			"source_app":       "HYD",
			"device_name":      "Chrome",
			"accept":           "application/json, text/plain, */*",
			"authorization":    "Bearer",
		},
	}
}
