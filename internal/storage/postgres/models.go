package postgres

import (
	"database/sql/driver"
	"encoding/json"
	"errors"

	"gorm.io/datatypes"
)

// Item represents an item stored in the database
// It uses JSONB to store arbitrary JSON payloads
type Item struct {
	ID      uint           `gorm:"primaryKey" json:"id"`
	Payload datatypes.JSON `gorm:"type:jsonb" json:"payload"`
}

// TableName specifies the table name for the Item model
func (Item) TableName() string {
	return "items"
}

// MarshalJSON customizes JSON serialization to return the payload content
func (i Item) MarshalJSON() ([]byte, error) {
	// Return the payload directly, not wrapped in an object
	if len(i.Payload) == 0 {
		return json.Marshal(map[string]interface{}{})
	}
	return i.Payload.MarshalJSON()
}

// UnmarshalJSON customizes JSON deserialization
func (i *Item) UnmarshalJSON(data []byte) error {
	// Store the raw JSON as the payload
	return i.Payload.UnmarshalJSON(data)
}

// Scan implements the sql.Scanner interface
func (i *Item) Scan(value interface{}) error {
	bytes, ok := value.([]byte)
	if !ok {
		return errors.New("failed to unmarshal JSONB value")
	}
	return json.Unmarshal(bytes, i)
}

// Value implements the driver.Valuer interface
func (i Item) Value() (driver.Value, error) {
	return json.Marshal(i)
}
