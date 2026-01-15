package config

import (
	"os"
	"strconv"
)

// Config holds all application configuration
type Config struct {
	// Server configuration
	Host string
	Port int

	// Database configuration
	DBDsn string

	// Test configuration
	TestPort int
}

// Load loads configuration from environment variables with sensible defaults
func Load() *Config {
	return &Config{
		Host:     getEnv("HOST", "0.0.0.0"),
		Port:     getEnvAsInt("PORT", 5001),
		DBDsn:    getEnv("DB_DSN", ""),
		TestPort: getEnvAsInt("TEST_PORT", 5001),
	}
}

// getEnv retrieves an environment variable or returns a default value
func getEnv(key, defaultValue string) string {
	value := os.Getenv(key)
	if value == "" {
		return defaultValue
	}
	return value
}

// getEnvAsInt retrieves an environment variable as an integer or returns a default value
func getEnvAsInt(key string, defaultValue int) int {
	valueStr := os.Getenv(key)
	if valueStr == "" {
		return defaultValue
	}
	value, err := strconv.Atoi(valueStr)
	if err != nil {
		return defaultValue
	}
	return value
}
