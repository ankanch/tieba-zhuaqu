package main

import (
	"fmt"
	"os"

	tiebascrapy "github.com/ankanch/tieba-zhuaqu/tiebascrapy/lib"
	log "github.com/sirupsen/logrus"
)

func main() {
	initWorker()

	fmt.Println(tiebascrapy.GetUUIDString())

	//create a job
	j := tiebascrapy.Job{Success: false,
		ErrMsg:    "",
		ID:        tiebascrapy.GenerateUUID(),
		TiebaName: "Dota2吧",
		PostName:  "DOTA2性价比饰品搭配大全，希望大家用的上",
		URL:       "https://tieba.baidu.com/p/6230479485",
		ProcFlow:  tiebascrapy.GetUUIDString()}

	tiebascrapy.WriteJobToFile(j)

	//execute Job
	resp := j.GetPage()
	pdl, success := tiebascrapy.ParsePosts(j, resp)
	if success == false {
		log.Error("main:failed to parse post data ")
	}
	tiebascrapy.WritePostDataListToFile(pdl)
}

func initWorker() {
	tiebascrapy.LoadConfiguration()

	//load or create uuid
	tiebascrapy.GenerateUUID()
	wuuid := tiebascrapy.GetConfStringValue("worker", "WORKER_UUID")
	if wuuid != "" {
		tiebascrapy.SetUUIDFromString(wuuid)
	}
	tiebascrapy.SetConfValue("worker", "WORKER_UUID", tiebascrapy.GetUUIDString())
	tiebascrapy.SaveConfiguration()

	//create dirs
	if _, err := os.Stat("cache"); os.IsNotExist(err) {
		os.Mkdir("cache", os.ModePerm)
	}
	if _, err := os.Stat("cache/jobs"); os.IsNotExist(err) {
		os.Mkdir("cache/jobs", os.ModePerm)
	}
	if _, err := os.Stat("cache/postdata"); os.IsNotExist(err) {
		os.Mkdir("cache/postdata", os.ModePerm)
	}

	//

}
