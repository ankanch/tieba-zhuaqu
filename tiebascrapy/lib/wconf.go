package tiebascrapy

import (
	"fmt"
	"os"

	"gopkg.in/ini.v1"
)

//WorkerConfigurationFile stores file handler of conf file in project root
var workerConfigurationFile *ini.File

//LoadConfiguration loads config file from project root path
func LoadConfiguration() {
	wcf, err := ini.Load("conf")
	if err != nil {
		fmt.Printf("Configuration file error -> fail to read file: %v", err)
		os.Exit(1)
	}
	workerConfigurationFile = wcf
}

//SaveConfiguration save current configuration to default conf file
func SaveConfiguration() {
	workerConfigurationFile.SaveTo("conf")
}

//GetConfiguration get current workerConfigurationFile object
func GetConfiguration() *ini.File {
	return workerConfigurationFile
}

//conf related functions
