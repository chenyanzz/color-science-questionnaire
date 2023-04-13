package config

type ServerType struct {
	Host string
	Port int
}

type MongoType struct {
	Uri      string
	Database string
}

type ConfigType struct {
	Server ServerType
	Mongo  MongoType
}
