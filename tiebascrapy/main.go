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
	tiebascrapy.LoadConfiguration()

	//load or create uuid
	tiebascrapy.GenerateUUID()
	wuuid := tiebascrapy.GetConfStringValue("worker", "WORKER_UUID")
	if wuuid != "" {
		tiebascrapy.SetUUIDFromString(wuuid)
	}
	tiebascrapy.SetConfValue("worker", "WORKER_UUID", tiebascrapy.GetUUIDString())
	tiebascrapy.SaveConfiguration()

}
