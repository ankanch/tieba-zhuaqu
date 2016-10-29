#pragma once


// CCreateJobDlg 对话框

class CCreateJobDlg : public CDialogEx
{
	DECLARE_DYNAMIC(CCreateJobDlg)

public:
	CCreateJobDlg(CWnd* pParent = NULL);   // 标准构造函数
	virtual ~CCreateJobDlg();
	CString tiebaName;
	int pages;

// 对话框数据
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_DIALOG_CREATE_JOB };
#endif

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV 支持

	DECLARE_MESSAGE_MAP()
public:
	afx_msg void OnBnClickedOk();
};
