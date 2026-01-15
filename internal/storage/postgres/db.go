package postgres

import (
	"fmt"
	"log"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

// DB wraps a GORM database connection
type DB struct {
	*gorm.DB
}

// Connect establishes a connection to PostgreSQL and runs migrations
func Connect(dsn string) (*DB, error) {
	if dsn == "" {
		return nil, fmt.Errorf("database DSN is required")
	}

	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{
		Logger: logger.Default.LogMode(logger.Silent),
	})
	if err != nil {
		return nil, fmt.Errorf("failed to connect to database: %w", err)
	}

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
