package tiebascrapy

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"

	"gopkg.in/ini.v1"
)

//WorkerConfigurationFile stores file handler of conf file in project root
var workerConfigurationFile *ini.File

//default values
var defalutCfgMap = map[string]interface{}{
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
		return defalutCfgMap[key].(string)
	}
	return v
}

//GetConfIntValue gets int value from conf file, return default(in defaultMap) if not exist
func GetConfIntValue(section string, key string) int {
	v, err := workerConfigurationFile.Section("worker").Key("WORKER_UUID").Int()
	if err != nil {
		return defalutCfgMap[key].(int)
	}
	return v
}

//GetConfBoolValue gets bool value from conf file, return default(in defaultMap) if not exist
func GetConfBoolValue(section string, key string) bool {
	v, err := workerConfigurationFile.Section("worker").Key("WORKER_UUID").Bool()
	if err != nil {
		return defalutCfgMap[key].(bool)
	}
	return v
}

//SetConfValue set conf value, convet to string before saving
func SetConfValue(section string, key string, value string) {
	workerConfigurationFile.Section(section).Key(key).SetValue(value)
}

//ReadJobFromFile read single job object from file
func ReadJobFromFile(path string) Job {
	file, _ := ioutil.ReadFile(path)
	j := Job{}
	_ = json.Unmarshal([]byte(file), &j)
	return j
}

//ReadJobListFromFile read a list of jobs  from file
func ReadJobListFromFile(path string) []Job {
	file, _ := ioutil.ReadFile(path)
	j := make([]Job, 1)
	_ = json.Unmarshal([]byte(file), &j)
	return j
}

//WriteJobToFile writes single job to file as json
func WriteJobToFile(j Job) {
	file, _ := json.MarshalIndent(j, "", " ")
	_ = ioutil.WriteFile("cache/jobs/job.json", file, 0644)
}

//WriteJobListToFile writes list of jobs to file as json
func WriteJobListToFile(js []Job) {
	file, _ := json.MarshalIndent(js, "", " ")
	_ = ioutil.WriteFile("cache/jobs/joblist.json", file, 0644)
}

//WritePostDataToFile writes a single PostData to file
func WritePostDataToFile(pd PostData) {
	file, _ := json.MarshalIndent(pd, "", " ")
	_ = ioutil.WriteFile("cache/postdata/postdata.json", file, 0644)
}

//WritePostDataListToFile writes a list of PostData to file
func WritePostDataListToFile(pdl []PostData) {
	file, _ := json.MarshalIndent(pdl, "", " ")
	_ = ioutil.WriteFile("cache/postdata/postdatalist.json", file, 0644)
}
