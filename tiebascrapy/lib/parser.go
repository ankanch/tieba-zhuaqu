package tiebascrapy

import (
	"net/http"

	"github.com/PuerkitoBio/goquery"
)

//selectors for posts
var postSelector = "#j_p_postlist > div"

// PostData sotres single reply in a post
type PostData struct {

	// which tieba this post belongs to
	TiebaName string

	// which post this post belongs to
	FatherPost string

	// who post it
	Author string

	// what did the user post
	Content string

	// when did the user post
	PostDate string

	// if it is a reply, who did the user reply to
	ReplyTO string

	// URL for this post
	PostLink string
}

//ParsePosts is a function to extract posts from downloaded webpage
func ParsePosts(resp *http.Response) ([]PostData, bool) {
	doc, err := goquery.NewDocumentFromResponse(resp)
	if err != nil {
		return nil, false
	}
	doc.Find(postSelector)

	return nil, true
}
