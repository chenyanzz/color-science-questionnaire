package main

import (
	"color-science-server/config"
	"color-science-server/database"
	"color-science-server/model"
	"fmt"
	"os"

	"github.com/gin-gonic/gin"
	"github.com/labstack/gommon/log"
)

func main() {
	config.Init()
	model.Init()
	database.InitDb()
	router := gin.Default()
	InitRouter(router)

	log.Info("Gin Server Started")
	err := router.Run(fmt.Sprintf("%s:%d", config.Server.Host, config.Server.Port))
	if err != nil {
		log.Errorf("Error while running Server: %s", err.Error())
		os.Exit(-1)
	}
}
