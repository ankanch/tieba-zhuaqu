// CreateJobDlg.cpp : 实现文件
//

#include "stdafx.h"
#include "KCrawlerControal.h"
#include "CreateJobDlg.h"
#include "afxdialogex.h"


// CCreateJobDlg 对话框

IMPLEMENT_DYNAMIC(CCreateJobDlg, CDialogEx)

CCreateJobDlg::CCreateJobDlg(CWnd* pParent /*=NULL*/)
	: CDialogEx(IDD_DIALOG_CREATE_JOB, pParent)
{

}

CCreateJobDlg::~CCreateJobDlg()
{
}

void CCreateJobDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
}


BEGIN_MESSAGE_MAP(CCreateJobDlg, CDialogEx)
	ON_BN_CLICKED(IDOK, &CCreateJobDlg::OnBnClickedOk)
END_MESSAGE_MAP()


// CCreateJobDlg 消息处理程序


void CCreateJobDlg::OnBnClickedOk()
{
	// TODO: 在此添加控件通知处理程序代码
	//CDialogEx::OnOK();
	CString cpages = _T("0");
	CString tbname = _T("NULL");
	GetDlgItemText(IDC_EDIT_TIEBANAME, tbname);
	GetDlgItemText(IDC_EDIT_TIEBAPAGE, cpages);
	int pg = _wtoi(cpages.GetBuffer());
	if (tbname == _T("") || pg < 1)
	{
		MessageBoxW(_T("请输入有效数据！"), _T("错误！"), MB_ICONERROR | MB_OK);
		return;
	}
	pages = pg;
	tiebaName = tbname;
	CDialogEx::OnOK();
}
