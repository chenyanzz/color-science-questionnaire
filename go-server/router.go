package main

import (
	"color-science-server/database"
	"color-science-server/model"
	"context"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/sirupsen/logrus"
)

func UploadForm(c *gin.Context) {
	form := model.Form{}
	if err := c.ShouldBind(&form); err != nil {
		logrus.Error(err)
		c.String(500, "fail to parse json")
		return
	}
	form.CreatedAt = time.Now()
	if _, err := database.DB.Collection("forms").InsertOne(context.Background(), form); err != nil {
		logrus.Error(err)
		c.String(500, "fail to insert data")
		return
	}
	c.String(200, "ok")
}

func InitRouter(g *gin.Engine) {
	g.GET("/ping", func(c *gin.Context) { c.String(200, "pong") })
	g.POST("/upload", UploadForm)
}
