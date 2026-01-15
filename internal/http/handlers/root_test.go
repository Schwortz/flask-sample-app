package handlers

import (
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/gin-gonic/gin"
)

func TestRoot(t *testing.T) {
	// Set Gin to test mode
	gin.SetMode(gin.TestMode)

	// Create handlers (without DB since root handler doesn't use it)
	h := &Handlers{}

	// Create a test router
	router := gin.New()
	router.GET("/", h.Root)

	// Create a test request
	req, err := http.NewRequest("GET", "/", nil)
	if err != nil {
		t.Fatalf("Failed to create request: %v", err)
	}

	// Create a response recorder
	rr := httptest.NewRecorder()

	// Serve the request
	router.ServeHTTP(rr, req)

	// Check status code
	if status := rr.Code; status != http.StatusOK {
		t.Errorf("Handler returned wrong status code: got %v want %v", status, http.StatusOK)
	}

	// Check response body
	expected := "Hello, Flask!"
	if rr.Body.String() != expected {
		t.Errorf("Handler returned unexpected body: got %v want %v", rr.Body.String(), expected)
	}

	// Check Content-Type header
	contentType := rr.Header().Get("Content-Type")
	expectedContentType := "text/html; charset=utf-8"
	if contentType != expectedContentType {
		t.Errorf("Handler returned wrong Content-Type: got %v want %v", contentType, expectedContentType)
	}
}
