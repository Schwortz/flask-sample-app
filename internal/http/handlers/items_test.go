package handlers

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/your-org/flask-sample-go/internal/core/items"
	"github.com/your-org/flask-sample-go/internal/storage/postgres"
)

// mockRepository is a mock implementation of the repository for testing
type mockRepository struct {
	items       []postgres.Item
	createError error
	findError   error
	nextID      uint
}

func newMockRepository() *mockRepository {
	return &mockRepository{
		items:  []postgres.Item{},
		nextID: 1,
	}
}

func (m *mockRepository) CreateItem(payload []byte) (*postgres.Item, error) {
	if m.createError != nil {
		return nil, m.createError
	}
	item := &postgres.Item{
		ID:      m.nextID,
		Payload: payload,
	}
	m.nextID++
	m.items = append(m.items, *item)
	return item, nil
}

func (m *mockRepository) FindAllItems() ([]postgres.Item, error) {
	if m.findError != nil {
		return nil, m.findError
	}
	return m.items, nil
}

func (m *mockRepository) FindItemByID(id uint) (*postgres.Item, error) {
	if m.findError != nil {
		return nil, m.findError
	}
	for _, item := range m.items {
		if item.ID == id {
			return &item, nil
		}
	}
	return nil, nil
}

func TestGetItems_EmptyList(t *testing.T) {
	gin.SetMode(gin.TestMode)

	// Create mock repository and service
	repo := newMockRepository()
	service := items.NewService(repo)
	h := NewHandlers(service)

	// Create router and register route
	router := gin.New()
	router.GET("/items", h.GetItems)

	// Create request
	req, _ := http.NewRequest("GET", "/items", nil)
	w := httptest.NewRecorder()

	// Serve request
	router.ServeHTTP(w, req)

	// Assertions
	if w.Code != http.StatusOK {
		t.Errorf("Expected status 200, got %d", w.Code)
	}

	var response map[string]interface{}
	if err := json.Unmarshal(w.Body.Bytes(), &response); err != nil {
		t.Fatalf("Failed to parse response: %v", err)
	}

	itemsList, ok := response["items"].([]interface{})
	if !ok {
		t.Fatalf("Expected 'items' key with array value")
	}

	if len(itemsList) != 0 {
		t.Errorf("Expected empty items array, got %d items", len(itemsList))
	}
}

func TestGetItems_WithMultipleItems(t *testing.T) {
	gin.SetMode(gin.TestMode)

	// Create mock repository with items
	repo := newMockRepository()
	item1Data := map[string]interface{}{"name": "item1", "value": 100}
	item2Data := map[string]interface{}{"name": "item2", "value": 200}

	item1JSON, _ := json.Marshal(item1Data)
	item2JSON, _ := json.Marshal(item2Data)

	repo.CreateItem(item1JSON)
	repo.CreateItem(item2JSON)

	// Create service and handlers
	service := items.NewService(repo)
	h := NewHandlers(service)

	// Create router
	router := gin.New()
	router.GET("/items", h.GetItems)

	// Create request
	req, _ := http.NewRequest("GET", "/items", nil)
	w := httptest.NewRecorder()

	// Serve request
	router.ServeHTTP(w, req)

	// Assertions
	if w.Code != http.StatusOK {
		t.Errorf("Expected status 200, got %d", w.Code)
	}

	var response map[string]interface{}
	if err := json.Unmarshal(w.Body.Bytes(), &response); err != nil {
		t.Fatalf("Failed to parse response: %v", err)
	}

	itemsList, ok := response["items"].([]interface{})
	if !ok {
		t.Fatalf("Expected 'items' key with array value")
	}

	if len(itemsList) != 2 {
		t.Errorf("Expected 2 items, got %d", len(itemsList))
	}

	// Verify first item
	firstItem := itemsList[0].(map[string]interface{})
	if firstItem["name"] != "item1" {
		t.Errorf("Expected first item name 'item1', got %v", firstItem["name"])
	}

	// Verify second item
	secondItem := itemsList[1].(map[string]interface{})
	if secondItem["name"] != "item2" {
		t.Errorf("Expected second item name 'item2', got %v", secondItem["name"])
	}

	// Verify Content-Type
	contentType := w.Header().Get("Content-Type")
	if contentType != "application/json; charset=utf-8" {
		t.Errorf("Expected Content-Type 'application/json; charset=utf-8', got '%s'", contentType)
	}
}

func TestGetItem_Success(t *testing.T) {
	gin.SetMode(gin.TestMode)

	// Create mock repository with an item
	repo := newMockRepository()
	itemData := map[string]interface{}{"name": "test_item", "description": "test"}
	itemJSON, _ := json.Marshal(itemData)
	repo.CreateItem(itemJSON)

	// Create service and handlers
	service := items.NewService(repo)
	h := NewHandlers(service)

	// Create router
	router := gin.New()
	router.GET("/items/:id", h.GetItem)

	// Create request
	req, _ := http.NewRequest("GET", "/items/1", nil)
	w := httptest.NewRecorder()

	// Serve request
	router.ServeHTTP(w, req)

	// Assertions
	if w.Code != http.StatusOK {
		t.Errorf("Expected status 200, got %d", w.Code)
	}

	var response map[string]interface{}
	if err := json.Unmarshal(w.Body.Bytes(), &response); err != nil {
		t.Fatalf("Failed to parse response: %v", err)
	}

	item, ok := response["item"].(map[string]interface{})
	if !ok {
		t.Fatalf("Expected 'item' key with object value")
	}

	if item["name"] != "test_item" {
		t.Errorf("Expected item name 'test_item', got %v", item["name"])
	}

	// Verify Content-Type
	contentType := w.Header().Get("Content-Type")
	if contentType != "application/json; charset=utf-8" {
		t.Errorf("Expected Content-Type 'application/json; charset=utf-8', got '%s'", contentType)
	}
}

func TestGetItem_NotFound(t *testing.T) {
	gin.SetMode(gin.TestMode)

	// Create mock repository with no items
	repo := newMockRepository()

	// Create service and handlers
	service := items.NewService(repo)
	h := NewHandlers(service)

	// Create router
	router := gin.New()
	router.GET("/items/:id", h.GetItem)

	// Create request for non-existent item
	req, _ := http.NewRequest("GET", "/items/999", nil)
	w := httptest.NewRecorder()

	// Serve request
	router.ServeHTTP(w, req)

	// Assertions
	if w.Code != http.StatusNotFound {
		t.Errorf("Expected status 404, got %d", w.Code)
	}

	var response map[string]interface{}
	if err := json.Unmarshal(w.Body.Bytes(), &response); err != nil {
		t.Fatalf("Failed to parse response: %v", err)
	}

	errorMsg, ok := response["error"].(string)
	if !ok {
		t.Fatalf("Expected 'error' key with string value")
	}

	if errorMsg != "Item not found" {
		t.Errorf("Expected error message 'Item not found', got '%s'", errorMsg)
	}
}

func TestGetItem_InvalidID(t *testing.T) {
	gin.SetMode(gin.TestMode)

	// Create mock repository
	repo := newMockRepository()

	// Create service and handlers
	service := items.NewService(repo)
	h := NewHandlers(service)

	// Create router
	router := gin.New()
	router.GET("/items/:id", h.GetItem)

	// Test with invalid ID (non-numeric)
	req, _ := http.NewRequest("GET", "/items/invalid", nil)
	w := httptest.NewRecorder()

	router.ServeHTTP(w, req)

	if w.Code != http.StatusNotFound {
		t.Errorf("Expected status 404 for invalid ID, got %d", w.Code)
	}
}

func TestPostItem_Success(t *testing.T) {
	gin.SetMode(gin.TestMode)

	// Create mock repository
	repo := newMockRepository()

	// Create service and handlers
	service := items.NewService(repo)
	h := NewHandlers(service)

	// Create router
	router := gin.New()
	router.POST("/items", h.PostItem)

	// Create request with JSON body
	itemData := map[string]interface{}{"name": "new_item", "value": 42}
	jsonData, _ := json.Marshal(itemData)
	req, _ := http.NewRequest("POST", "/items", bytes.NewBuffer(jsonData))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()

	// Serve request
	router.ServeHTTP(w, req)

	// Assertions
	if w.Code != http.StatusCreated {
		t.Errorf("Expected status 201, got %d", w.Code)
	}

	var response map[string]interface{}
	if err := json.Unmarshal(w.Body.Bytes(), &response); err != nil {
		t.Fatalf("Failed to parse response: %v", err)
	}

	message, ok := response["message"].(string)
	if !ok {
		t.Fatalf("Expected 'message' key with string value")
	}

	if message != "Item added successfully" {
		t.Errorf("Expected message 'Item added successfully', got '%s'", message)
	}

	// Verify item was actually added to repository
	allItems, _ := repo.FindAllItems()
	if len(allItems) != 1 {
		t.Errorf("Expected 1 item in repository, got %d", len(allItems))
	}
}

func TestPostItem_EmptyObject(t *testing.T) {
	gin.SetMode(gin.TestMode)

	// Create mock repository
	repo := newMockRepository()

	// Create service and handlers
	service := items.NewService(repo)
	h := NewHandlers(service)

	// Create router
	router := gin.New()
	router.POST("/items", h.PostItem)

	// Create request with empty JSON object
	req, _ := http.NewRequest("POST", "/items", bytes.NewBufferString("{}"))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()

	// Serve request
	router.ServeHTTP(w, req)

	// Assertions - empty object should be accepted per test_integration.py:169
	if w.Code != http.StatusCreated {
		t.Errorf("Expected status 201, got %d", w.Code)
	}

	var response map[string]interface{}
	if err := json.Unmarshal(w.Body.Bytes(), &response); err != nil {
		t.Fatalf("Failed to parse response: %v", err)
	}

	if response["message"] != "Item added successfully" {
		t.Errorf("Expected success message for empty object")
	}
}

func TestPostItem_ComplexNestedData(t *testing.T) {
	gin.SetMode(gin.TestMode)

	// Create mock repository
	repo := newMockRepository()

	// Create service and handlers
	service := items.NewService(repo)
	h := NewHandlers(service)

	// Create router
	router := gin.New()
	router.POST("/items", h.PostItem)

	// Create request with complex nested data
	complexData := map[string]interface{}{
		"name": "complex_item",
		"metadata": map[string]interface{}{
			"tags":     []string{"tag1", "tag2"},
			"settings": map[string]interface{}{"enabled": true, "count": 5},
		},
		"numbers": []int{1, 2, 3, 4, 5},
	}
	jsonData, _ := json.Marshal(complexData)
	req, _ := http.NewRequest("POST", "/items", bytes.NewBuffer(jsonData))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()

	// Serve request
	router.ServeHTTP(w, req)

	// Assertions
	if w.Code != http.StatusCreated {
		t.Errorf("Expected status 201, got %d", w.Code)
	}

	// Verify the complex data was stored correctly
	allItems, _ := repo.FindAllItems()
	if len(allItems) != 1 {
		t.Fatalf("Expected 1 item, got %d", len(allItems))
	}

	var storedData map[string]interface{}
	json.Unmarshal(allItems[0].Payload, &storedData)

	if storedData["name"] != "complex_item" {
		t.Errorf("Complex data not stored correctly")
	}
}

func TestPostItem_InvalidJSON(t *testing.T) {
	gin.SetMode(gin.TestMode)

	// Create mock repository
	repo := newMockRepository()

	// Create service and handlers
	service := items.NewService(repo)
	h := NewHandlers(service)

	// Create router
	router := gin.New()
	router.POST("/items", h.PostItem)

	// Create request with invalid JSON
	req, _ := http.NewRequest("POST", "/items", bytes.NewBufferString("invalid json"))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()

	// Serve request
	router.ServeHTTP(w, req)

	// Assertions
	if w.Code != http.StatusBadRequest {
		t.Errorf("Expected status 400 for invalid JSON, got %d", w.Code)
	}

	var response map[string]interface{}
	if err := json.Unmarshal(w.Body.Bytes(), &response); err != nil {
		t.Fatalf("Failed to parse error response: %v", err)
	}

	if _, ok := response["error"]; !ok {
		t.Errorf("Expected error field in response for invalid JSON")
	}
}
