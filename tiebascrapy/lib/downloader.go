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
	errMsg string

	//Job ID
	ID uuid.UUID

	//Job url
	URL string

	// sotres machine that processed this Job
	// FIFO, last one must be either successed or failed,
	//		 the others must be fail processing ones.
	ProcFlow []uuid.UUID
}

//GetPage is a function to get a post webpage
func (j *Job) GetPage() *http.Response {
	resp, err := http.Get(j.URL)
	if err != nil {
		j.Success = false
		j.errMsg = ""
		return nil
	}
	defer resp.Body.Close()

	j.Success = true
	return resp
}
