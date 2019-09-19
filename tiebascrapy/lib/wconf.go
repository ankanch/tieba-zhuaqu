package tiebascrapy

import (
	"fmt"
	"os"

	"gopkg.in/ini.v1"
)

//WorkerConfigurationFile stores file handler of conf file in project root
var workerConfigurationFile *ini.File

//default values
var defalutMap = map[string]interface{}{
	"WORKER_UUID":                    "",
	"MAX_DOWNLOADER":                 4,
	"MAX_PARSER":                     2,
	"MAX_JOB_QUEUE":                  1000,
	"MAX_JOB_RETRIES":                3,
	"GETPAGE_TIMEOUT":                15,
	"COORDINATOR_DISCOVERY":          true,
	"COORDINATOR_DISCOVERY_INTERVAL": 60,
	"USE_DATABASE":                   false,
	"DATA_STORE":                     "csv",
}

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

//GetConfStringValue gets string value from conf file, return default(in defaultMap) if not exist
func GetConfStringValue(section string, key string) string {
	v := workerConfigurationFile.Section(section).Key(key).String()
	if v == "" {
		return defalutMap[key].(string)
	}
	return v
}

//GetConfIntValue gets int value from conf file, return default(in defaultMap) if not exist
func GetConfIntValue(section string, key string) int {
	v, err := workerConfigurationFile.Section("worker").Key("WORKER_UUID").Int()
	if err != nil {
		return defalutMap[key].(int)
	}
	return v
}

//GetConfBoolValue gets bool value from conf file, return default(in defaultMap) if not exist
func GetConfBoolValue(section string, key string) bool {
	v, err := workerConfigurationFile.Section("worker").Key("WORKER_UUID").Bool()
	if err != nil {
		return defalutMap[key].(bool)
	}
	return v
}

//SetConfValue set conf value, convet to string before saving
func SetConfValue(section string, key string, value string) {
	workerConfigurationFile.Section(section).Key(key).SetValue(value)
}
