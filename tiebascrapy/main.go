package main

import (
	"fmt"

	tiebascrapy "github.com/ankanch/tieba-zhuaqu/tiebascrapy/lib"
)

func main() {
	initWorker()

	fmt.Println(tiebascrapy.GetUUIDString())

}

func initWorker() {
	tiebascrapy.loadConfiguration()

	//load or create uuid
	tiebascrapy.GenerateUUID()
	wuuid := tiebascrapy.GetConfiguration().Section("worker").Key("WORKER_UUID").String()
	if wuuid != "" {
		tiebascrapy.SetUUIDFromString(wuuid)
	}
	tiebascrapy.GetConfiguration().Section("worker").Key("WORKER_UUID").SetValue((tiebascrapy.GetUUIDString()))
	tiebascrapy.saveConfiguration()

}
