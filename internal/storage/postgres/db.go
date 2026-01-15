package postgres

import (
	"context"
	"fmt"
	"log"
	"time"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

// DB wraps a GORM database connection
type DB struct {
	*gorm.DB
}

// Connect establishes a connection to PostgreSQL and runs migrations
// Uses a timeout to avoid blocking the application startup
func Connect(dsn string) (*DB, error) {
	if dsn == "" {
		return nil, fmt.Errorf("database DSN is required")
	}

	// Create a context with timeout for connection attempt
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()

	// Open database with GORM
	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{
		Logger: logger.Default.LogMode(logger.Silent),
	})
	if err != nil {
		return nil, fmt.Errorf("failed to connect to database: %w", err)
	}

	// Get underlying SQL DB to test connection with timeout
	sqlDB, err := db.DB()
	if err != nil {
		return nil, fmt.Errorf("failed to get database instance: %w", err)
	}

	// Test the connection with context timeout
	if err := sqlDB.PingContext(ctx); err != nil {
		return nil, fmt.Errorf("failed to ping database: %w", err)
	}

	// Set connection pool settings
	sqlDB.SetMaxOpenConns(10)
	sqlDB.SetMaxIdleConns(5)
	sqlDB.SetConnMaxLifetime(time.Hour)

	// Run auto-migration
	if err := db.AutoMigrate(&Item{}); err != nil {
		return nil, fmt.Errorf("failed to run migrations: %w", err)
	}

	log.Println("Database connected and migrations completed")

	return &DB{DB: db}, nil
}

// CreateItem creates a new item in the database
func (db *DB) CreateItem(payload []byte) (*Item, error) {
	item := &Item{
		Payload: payload,
	}

	if err := db.Create(item).Error; err != nil {
		return nil, fmt.Errorf("failed to create item: %w", err)
	}

	return item, nil
}

// FindAllItems retrieves all items from the database
func (db *DB) FindAllItems() ([]Item, error) {
	var items []Item
	if err := db.Find(&items).Error; err != nil {
		return nil, fmt.Errorf("failed to find items: %w", err)
	}
	return items, nil
}

// FindItemByID retrieves an item by its ID
func (db *DB) FindItemByID(id uint) (*Item, error) {
	var item Item
	if err := db.First(&item, id).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			return nil, nil // Return nil instead of error for not found
		}
		return nil, fmt.Errorf("failed to find item: %w", err)
	}
	return &item, nil
}
