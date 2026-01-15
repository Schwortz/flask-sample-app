package handlers

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

// Root handles GET / and returns "Hello, Flask!"
func (h *Handlers) Root(c *gin.Context) {
	// Set Content-Type to match Flask's behavior
	c.Data(http.StatusOK, "text/html; charset=utf-8", []byte("Hello, Flask!"))
}
