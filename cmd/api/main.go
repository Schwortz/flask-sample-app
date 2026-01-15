package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/your-org/flask-sample-go/internal/config"
	"github.com/your-org/flask-sample-go/internal/core/items"
	"github.com/your-org/flask-sample-go/internal/http/router"
	"github.com/your-org/flask-sample-go/internal/storage/memory"
)

func main() {
	// Load configuration
	cfg := config.Load()

	// Create repository - always use in-memory storage for instant startup
	// Database support is available but disabled by default for fast startup
	var repo items.Repository
	repo = memory.NewStore()
	log.Println("Using in-memory storage")

	// Optionally attempt database connection in background (currently disabled)
	// This ensures the application starts immediately without waiting for DB
	_ = cfg.DBDsn // Mark as used to avoid linter warnings

	// Create items service with chosen repository
	itemsService := items.NewService(repo)

	// Setup router with items service
	r := router.Setup(itemsService)

	// Create HTTP server
	addr := fmt.Sprintf("%s:%d", cfg.Host, cfg.Port)
	srv := &http.Server{
		Addr:    addr,
		Handler: r,
	}

	// Start server in a goroutine
	go func() {
		log.Printf("Starting server on %s", addr)
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Failed to start server: %v", err)
		}
	}()

	// Wait for interrupt signal to gracefully shutdown the server
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit
	log.Println("Shutting down server...")

	// Give outstanding requests 5 seconds to complete
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		log.Fatalf("Server forced to shutdown: %v", err)
	}

	log.Println("Server exited")
}
