package main

import (
	"fmt"
	"os"

	tiebascrapy "github.com/ankanch/tieba-zhuaqu/tiebascrapy/lib"
	"gopkg.in/ini.v1"
)

//WorkerConfigurationFile stores file handler of conf file in project root
var workerConfigurationFile *ini.File

func main() {
	initWorker()

	fmt.Println(tiebascrapy.WorkerUUID)

}

func initWorker() {
	tiebascrapy.GenerateUUID()
	workerConfigurationFile = loadConfiguration()
}

//LoadConfiguration loads config file from project root path
func loadConfiguration() *ini.File {
	workerConfigurationFile, err := ini.Load("conf")
	if err != nil {
		fmt.Printf("Configuration file error -> fail to read file: %v", err)
		os.Exit(1)
	}
	return workerConfigurationFile
}

//SaveConfiguration save current configuration to default conf file
func saveConfiguration() {
	workerConfigurationFile.SaveTo("conf")
}
