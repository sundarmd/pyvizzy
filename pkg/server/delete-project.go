package server

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/rbren/go-prompter/pkg/files"
	"github.com/sirupsen/logrus"

	"github.com/rbren/vizzy/pkg/keys"
)

func deleteProject(c *gin.Context) {
	projectID := c.Param("projectID")
	if projectID == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Project ID is required"})
		return
	}

	s3 := files.GetFileManager()
	err := s3.DeleteRecursive(keys.GetProjectDirectoryKey(projectID))
	if err != nil {
		logrus.WithError(err).Error("Failed to delete project")
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"success": true})
}
