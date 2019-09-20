package tiebascrapy

//PostDataField stores raw data-field attribution of post div
type PostDataField struct {
	/* This struct represents json object below, which can be extract from post data-field attribution
	{
		"author": {
			"user_id": 775687193,
			"user_name": "\u5012\u9709\u7684\u673d\u6728",
			"props": null,
			"portrait": "190ce58092e99c89e79a84e69cbde69ca83c2e",
			"user_nickname": null
		},
		"content": {
			"post_id": 127160443064,
			"is_anonym": false,
			"forum_id": 1627732,
			"thread_id": 6230479485,
			"content": "<img class=\"BDE_Image\" pic_type=\"0\" width=\"560\" height=\"408\" src=\"https:\/\/imgsa.baidu.com\/forum\/w%3D580\/sign=69f353ba0723dd542173a760e10bb3df\/724141ee3d6d55fb101b59f863224f4a22a4dd61.jpg\" >\u5982\u679c\u4f60\u6709\u94b1\uff0c\u4e5f\u53ef\u4ee5\u9009\u62e9\u8fd9\u4ef6\u6b66\u5668\uff08\u5851\u9020\u8005\u5723\u7269\uff09\u81ea\u8eab\u7684\u6548\u679c\u4e5f\u975e\u5e38\u4e0d\u9519\uff0c\u4f46\u662f\u4ef7\u683c\u6bd4\u8f83\u8d35\uff0c\u5176\u5b9e\u5728\u6240\u6709\u9970\u54c1\u4e2d\uff0c\u4e0d\u7b97\u8d35\u7684\uff0c\u4f46\u662f\u7ed9\u5927\u725b\u8fd9\u4e48\u4e00\u4e2a\u82f1\u96c4\u82b1\u94b1\uff0c\u6211\u5c31\u4e2a\u4eba\u8ba4\u4e3a\u4e0d\u662f\u5f88\u5212\u7b97\uff0c\u6240\u4ee5\u5982\u679c\u4f60\u559c\u6b22\uff0c\u53ef\u4ee5\u9009\u62e9\uff0c\u5982\u679c\u6ca1\u6709\u7ecf\u6d4e\u652f\u6301\uff0c\u8fd8\u662f\u53ef\u4ee5\u8003\u8651\u4e0a\u9762\u90a3\u5957\u54e6",
			"post_no": 7,
			"type": "0",
			"comment_num": 6,
			"is_fold": 0,
			"props": null,
			"post_index": 6,
			"pb_tpoint": null
		}
	}
	*/
	//Author stores author related data
	Author PostAuthor `json:"author"`

	//Content stores content related data
	Content PostContent `json:"content"`
}

//PostAuthor a representation of "author" json object in tieba post data-field
type PostAuthor struct {
	/* sample json:
		"author": {
		"user_id": 775687193,
		"user_name": "\u5012\u9709\u7684\u673d\u6728",
		"props": null,
		"portrait": "190ce58092e99c89e79a84e69cbde69ca83c2e",
		"user_nickname": null
	}
	*/
	UserID int `json:"user_id"`

	UserName string `json:"user_name"`

	Props string `json:"props"`

	Portrait string `json:"portrait"`

	UserNickname string `json:"user_nickname"`
}

//PostContent a representation of "content" json object in tieba post data-field
type PostContent struct {
	/* sample json:
		"content": {
		"post_id": 127160443064,
		"is_anonym": false,
		"forum_id": 1627732,
		"thread_id": 6230479485,
		"content": "<img class=\"BDE_Image\" pic_type=\"0\" width=\"560\" height=\"408\" src=\"https:\/\/imgsa.baidu.com\/forum\/w%3D580\/sign=69f353ba0723dd542173a760e10bb3df\/724141ee3d6d55fb101b59f863224f4a22a4dd61.jpg\" >\u5982\u679c\u4f60\u6709\u94b1\uff0c\u4e5f\u53ef\u4ee5\u9009\u62e9\u8fd9\u4ef6\u6b66\u5668\uff08\u5851\u9020\u8005\u5723\u7269\uff09\u81ea\u8eab\u7684\u6548\u679c\u4e5f\u975e\u5e38\u4e0d\u9519\uff0c\u4f46\u662f\u4ef7\u683c\u6bd4\u8f83\u8d35\uff0c\u5176\u5b9e\u5728\u6240\u6709\u9970\u54c1\u4e2d\uff0c\u4e0d\u7b97\u8d35\u7684\uff0c\u4f46\u662f\u7ed9\u5927\u725b\u8fd9\u4e48\u4e00\u4e2a\u82f1\u96c4\u82b1\u94b1\uff0c\u6211\u5c31\u4e2a\u4eba\u8ba4\u4e3a\u4e0d\u662f\u5f88\u5212\u7b97\uff0c\u6240\u4ee5\u5982\u679c\u4f60\u559c\u6b22\uff0c\u53ef\u4ee5\u9009\u62e9\uff0c\u5982\u679c\u6ca1\u6709\u7ecf\u6d4e\u652f\u6301\uff0c\u8fd8\u662f\u53ef\u4ee5\u8003\u8651\u4e0a\u9762\u90a3\u5957\u54e6",
		"post_no": 7,
		"type": "0",
		"comment_num": 6,
		"is_fold": 0,
		"props": null,
		"post_index": 6,
		"pb_tpoint": null
	}
	*/

	PostID int `json:"post_id"`

	IsAnonym bool `json:"is_anonym"`

	ForumID int `json:"forum_id"`

	ThreadID int `json:"thread_id"`

	Content string `json:"content"`

	PostNo int `json:"post_no"`

	Type string `json:"type"`

	CommentNum int `json:"comment_num"`

	IsFold int `json:"is_fold"`

	Props string `json:"props"`

	PostIndex int `json:"post_index"`

	PbTpoint string `json:"pb_tpoint"`
}
