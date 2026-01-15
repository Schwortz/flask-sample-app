package handlers

import (
	"github.com/your-org/flask-sample-go/internal/storage/postgres"
)

// Handlers holds dependencies for all HTTP handlers
type Handlers struct {
	db *postgres.DB
}

// NewHandlers creates a new Handlers instance with the given database connection
func NewHandlers(db *postgres.DB) *Handlers {
	return &Handlers{
		db: db,
	}
}
