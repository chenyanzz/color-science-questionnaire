package config

import (
	log "github.com/sirupsen/logrus"
	"github.com/spf13/viper"
)

var (
	Server ServerType
	Mongo  MongoType
)

func Init() {
	log.Info("[config] Init...")
	config := ConfigType{}
	viper.AddConfigPath(".")
	viper.SetConfigName("config")
	viper.SetConfigType("yaml")

	err := viper.ReadInConfig()
	if err != nil {
		log.Fatalf("Error in ReadInConfig: %s", err)
		return
	}

	err = viper.Unmarshal(&config)
	if err != nil {
		log.Fatalf("Error in Unmarshal: %s", err)
		return
	}

	Server = config.Server
	Mongo = config.Mongo

	if err != nil {
		log.Warnf("SessionSecret set failed: %s", err)
	}
	log.Info("[Config] Init success")
}
