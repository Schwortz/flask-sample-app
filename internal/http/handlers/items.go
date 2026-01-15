package handlers

import (
	"encoding/json"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
)

// GetItems handles GET /items and returns all items
func (h *Handlers) GetItems(c *gin.Context) {
	items, err := h.db.FindAllItems()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to retrieve items"})
		return
	}

	// Convert items to []interface{} to match Flask's JSON format
	itemList := make([]interface{}, len(items))
	for i, item := range items {
		var payload interface{}
		if err := json.Unmarshal(item.Payload, &payload); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to parse item"})
			return
		}
		itemList[i] = payload
	}

	c.JSON(http.StatusOK, gin.H{"items": itemList})
}

// GetItem handles GET /items/:id and returns a single item by ID
func (h *Handlers) GetItem(c *gin.Context) {
	idStr := c.Param("id")
	id, err := strconv.ParseUint(idStr, 10, 32)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Item not found"})
		return
	}

	item, err := h.db.FindItemByID(uint(id))
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to retrieve item"})
		return
	}

	if item == nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Item not found"})
		return
	}

	// Parse the payload
	var payload interface{}
	if err := json.Unmarshal(item.Payload, &payload); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to parse item"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"item": payload})
}

// AddItem handles POST /items and creates a new item
func (h *Handlers) AddItem(c *gin.Context) {
	var rawPayload json.RawMessage
	if err := c.ShouldBindJSON(&rawPayload); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid JSON"})
		return
	}

	_, err := h.db.CreateItem(rawPayload)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create item"})
		return
	}

	c.JSON(http.StatusCreated, gin.H{"message": "Item added successfully"})
}
