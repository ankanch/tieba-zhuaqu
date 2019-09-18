package scrapylib

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
func ParsePosts(respBody []byte) ([]PostData, bool) {
	bodyText := string(respBody)

}
