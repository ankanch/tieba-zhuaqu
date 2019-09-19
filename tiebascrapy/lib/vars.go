package tiebascrapy

import (
	uuid "github.com/satori/go.uuid"
)

//WorkerUUID indicate current worker UUID
var WorkerUUID uuid.UUID

var uuidGot = false

//GenerateUUID can get UUID based on MAC address and timestamp
func GenerateUUID() {
	if uuidGot == false {
		WorkerUUID = uuid.NewV1()
		uuidGot = true
	}
}
