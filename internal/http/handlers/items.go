package handlers

import (
	"encoding/json"
	"errors"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/your-org/flask-sample-go/internal/core/items"
)

// GetItems handles GET /items and returns all items
func (h *Handlers) GetItems(c *gin.Context) {
	itemList, err := h.itemsService.GetAllItems()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to retrieve items"})
		return
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

	item, err := h.itemsService.GetItemByID(uint(id))
	if err != nil {
		if errors.Is(err, items.ItemNotFoundError) {
			c.JSON(http.StatusNotFound, gin.H{"error": "Item not found"})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to retrieve item"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"item": item})
}

// PostItem handles POST /items and creates a new item
func (h *Handlers) PostItem(c *gin.Context) {
	var rawPayload json.RawMessage
	if err := c.ShouldBindJSON(&rawPayload); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid JSON"})
		return
	}

	err := h.itemsService.CreateItem(rawPayload)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create item"})
		return
	}

	c.JSON(http.StatusCreated, gin.H{"message": "Item added successfully"})
}
