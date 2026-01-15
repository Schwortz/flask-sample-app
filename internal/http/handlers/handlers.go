package handlers

import (
	"github.com/your-org/flask-sample-go/internal/core/items"
)

// Handlers holds dependencies for all HTTP handlers
type Handlers struct {
	itemsService *items.Service
}

// NewHandlers creates a new Handlers instance with the given items service
func NewHandlers(itemsService *items.Service) *Handlers {
	return &Handlers{
		itemsService: itemsService,
	}
}
