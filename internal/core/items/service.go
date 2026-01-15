package items

import (
	"encoding/json"
	"errors"

	"github.com/your-org/flask-sample-go/internal/storage/postgres"
)

// ItemNotFoundError is returned when an item is not found
var ItemNotFoundError = errors.New("item not found")

// Repository defines the interface for item data access
type Repository interface {
	CreateItem(payload []byte) (*postgres.Item, error)
	FindAllItems() ([]postgres.Item, error)
	FindItemByID(id uint) (*postgres.Item, error)
}

// Service handles business logic for items
type Service struct {
	repo Repository
}

// NewService creates a new items service
func NewService(repo Repository) *Service {
	return &Service{
		repo: repo,
	}
}

// GetAllItems retrieves all items and returns them as a slice of interfaces
func (s *Service) GetAllItems() ([]interface{}, error) {
	items, err := s.repo.FindAllItems()
	if err != nil {
		return nil, err
	}

	// Convert items to []interface{} to match Flask's JSON format
	itemList := make([]interface{}, len(items))
	for i, item := range items {
		var payload interface{}
		if err := json.Unmarshal(item.Payload, &payload); err != nil {
			return nil, err
		}
		itemList[i] = payload
	}

	return itemList, nil
}

// GetItemByID retrieves a single item by its ID
func (s *Service) GetItemByID(id uint) (interface{}, error) {
	item, err := s.repo.FindItemByID(id)
	if err != nil {
		return nil, err
	}

	if item == nil {
		return nil, ItemNotFoundError
	}

	// Parse the payload
	var payload interface{}
	if err := json.Unmarshal(item.Payload, &payload); err != nil {
		return nil, err
	}

	return payload, nil
}

// CreateItem creates a new item with the given payload
func (s *Service) CreateItem(payload []byte) error {
	_, err := s.repo.CreateItem(payload)
	return err
}
