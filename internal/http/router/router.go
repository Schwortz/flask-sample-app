package router

import (
	"github.com/gin-gonic/gin"
	"github.com/your-org/flask-sample-go/internal/http/handlers"
	"github.com/your-org/flask-sample-go/internal/storage/postgres"
)

// Setup creates and configures the Gin router with all routes and middleware
func Setup(db *postgres.DB) *gin.Engine {
	// Set Gin to release mode to reduce verbosity
	gin.SetMode(gin.ReleaseMode)

	router := gin.New()

	// Add middleware
	router.Use(gin.Logger())   // Log all requests
	router.Use(gin.Recovery()) // Recover from panics

	// Create handlers with database dependency
	h := handlers.NewHandlers(db)

	// Register routes
	router.GET("/", h.Root)
	router.GET("/items", h.GetItems)
	router.GET("/items/:id", h.GetItem)
	router.POST("/items", h.AddItem)

	return router
}
