package memory

import (
	"encoding/json"
	"sync"

	"github.com/your-org/flask-sample-go/internal/storage/postgres"
)

// Store provides an in-memory storage for items
type Store struct {
	mu    sync.RWMutex
	items []postgres.Item
	nextID uint
}

// NewStore creates a new in-memory store
func NewStore() *Store {
	return &Store{
		items: make([]postgres.Item, 0),
		nextID: 1,
	}
}

// CreateItem creates a new item in memory
func (s *Store) CreateItem(payload []byte) (*postgres.Item, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	// Validate that payload is valid JSON
	var temp interface{}
	if err := json.Unmarshal(payload, &temp); err != nil {
		return nil, err
	}

	item := postgres.Item{
		ID: s.nextID,
	}
	// Copy payload to ensure it's stored properly
	item.Payload = make([]byte, len(payload))
	copy(item.Payload, payload)
	s.items = append(s.items, item)
	s.nextID++

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

// FindItemByID retrieves an item by its ID from memory
func (s *Store) FindItemByID(id uint) (*postgres.Item, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()

	for _, item := range s.items {
		if item.ID == id {
			return &item, nil
		}
	}
	return nil, nil // Return nil if not found
}
