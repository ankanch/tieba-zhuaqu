package tiebascrapy

import (
	uuid "github.com/satori/go.uuid"
)

//WorkerUUID indicate current worker UUID
var workerUUID uuid.UUID

var uuidGot = false

//GenerateUUID can get UUID based on MAC address and timestamp
func GenerateUUID() uuid.UUID {
	if uuidGot == false {
		workerUUID = uuid.NewV1()
		uuidGot = true
		return workerUUID
	}
	return uuid.NewV1()
}

//SetUUIDFromString set UUID from string, return false if parsed error
func SetUUIDFromString(uuidstr string) bool {
	v, err := uuid.FromString(uuidstr)
	if err != nil {
		return false
	}
	workerUUID = v
	return true
}

//SetUUID set UUID from []byte
func SetUUID(uuidbyte uuid.UUID) {
	workerUUID = uuidbyte
}

//GetUUIDString get uuid in string
func GetUUIDString() string {
	return workerUUID.String()
}

//GetUUID gets UUID in [16]byte
func GetUUID() uuid.UUID {
	return workerUUID
}
