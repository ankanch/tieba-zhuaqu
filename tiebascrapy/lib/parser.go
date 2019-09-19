package tiebascrapy

import (
	"fmt"
	"net/http"

	"github.com/PuerkitoBio/goquery"
	log "github.com/sirupsen/logrus"
)

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

	// where this post lives
	FloorNum string

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
	defer resp.Body.Close()
	if err != nil {
		log.Error("ParsePosts:failed to create new document from response")
		return nil, false
	}
	//
	parseFloorNumAndPostDate := func(s *goquery.Selection) (floorNum string, postDate string) {
		v0 := s.Find(".post-tail-wrap > span:nth-child(2)").Text()
		v1 := s.Find(".post-tail-wrap > span:nth-child(3)").Text()
		v2 := s.Find(".post-tail-wrap > span:nth-child(4)").Text()
		if v2 == "" {
			/* there are two types of post-tail-wrap:
			*		1. with in-floor replies
			*		2. without in-floor replies
			* for scenario 1, 3 nested spans in div:#post-tail-warp, with #2 is floor num and #3 is post date
			* for scenario 2, 4 nested ones there with #3 is floor number and #4 is post date
			 */
			return v0, v1
		}
		return v1, v2
	}
	//
	pdl := make([]PostData, 0)
	doc.Find(SelectorFloorList).Each(
		func(i int, s *goquery.Selection) {
			floorNum, postDate := parseFloorNumAndPostDate(s)

			pd := PostData{
				TiebaName:  "",
				FatherPost: "",
				Author:     s.Find(SelectorFloorAuthor).Text(),
				Content:    s.Find(SelectorFloorContent).Text(),
				FloorNum:   floorNum,
				PostDate:   postDate,
				ReplyTO:    "",
				PostLink:   "",
			}
			pdl = append(pdl, pd)
			band := s.Find(".post-tail-wrap > span:nth-child(4)").Text()

			fmt.Printf("Review %d: %s\n", i, band)
		})

	return pdl, true
}
