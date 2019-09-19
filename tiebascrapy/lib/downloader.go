package tiebascrapy

import (
	"net/http"

	uuid "github.com/satori/go.uuid"
)

//Job is a basic representation of a posting page processing
type Job struct {

	//indicates if this job finished successfully.
	Success bool

	// error message if unsuccess
	ErrMsg string

	//Job ID
	ID uuid.UUID

	//Job url
	URL string

	// sotres machine that processed this Job
	// FIFO, last one must be either successed or failed,
	//		 the others must be failed in processing this job.
	// workers are arranged as uuid1->uuid2->uuid3->...->uuidn
	ProcFlow string
}

//GetPage is a function to get a post webpage
func (j *Job) GetPage() *http.Response {
	resp, err := http.Get(j.URL)
	if err != nil {
		j.Success = false
		j.ErrMsg = ""
		return nil
	}
	j.Success = true
	return resp
}
