package memory

import (
	"encoding/json"
	"sync"

	"github.com/your-org/flask-sample-go/internal/storage/postgres"
)

// Store provides an in-memory storage for items
// Uses 0-based indices to match the original Python Flask app behavior
type Store struct {
	mu    sync.RWMutex
	items []postgres.Item
}

// NewStore creates a new in-memory store
func NewStore() *Store {
	return &Store{
		items: make([]postgres.Item, 0),
	}
}

// CreateItem creates a new item in memory
// The ID field is set to the array index (0-based) to match Python Flask app behavior
func (s *Store) CreateItem(payload []byte) (*postgres.Item, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	// Validate that payload is valid JSON
	var temp interface{}
	if err := json.Unmarshal(payload, &temp); err != nil {
		return nil, err
	}

	// Use the current length as the index (0-based)
	itemIndex := uint(len(s.items))

	item := postgres.Item{
		ID: itemIndex,
	}
	// Copy payload to ensure it's stored properly
	item.Payload = make([]byte, len(payload))
	copy(item.Payload, payload)
	s.items = append(s.items, item)

	return &item, nil
}

// FindAllItems retrieves all items from memory
func (s *Store) FindAllItems() ([]postgres.Item, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()

	// Return a copy to avoid external modifications
	result := make([]postgres.Item, len(s.items))
	copy(result, s.items)
	return result, nil
}

// FindItemByID retrieves an item by its index (0-based) from memory
// This matches the Python Flask app behavior where item_id is the array index
func (s *Store) FindItemByID(id uint) (*postgres.Item, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()

	// Treat id as an array index (0-based)
	if id < uint(len(s.items)) {
		return &s.items[id], nil
	}
	return nil, nil // Return nil if index is out of bounds
}
