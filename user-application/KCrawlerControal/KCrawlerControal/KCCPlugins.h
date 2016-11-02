#pragma once
#include "afxwin.h"


// KCCPlugins 对话框

struct Plugin {
	CString name;
	CString descri;
	CString exefilename;
};

class KCCPlugins : public CDialogEx
{
	DECLARE_DYNAMIC(KCCPlugins)

public:
	KCCPlugins(CWnd* pParent = NULL);   // 标准构造函数
	virtual ~KCCPlugins();

// 对话框数据
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_DIALOG_USE_PLUGINS };
#endif

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV 支持

	DECLARE_MESSAGE_MAP()

public:
	//Python插件相关
	CString PATH_PLUGINS_INDEX_FILE = _T("plugins.list");
	Plugin *pluginlist;
	void loadPlugins();   //加载插件（包括创建按钮与关联按钮事件）
	void setupBasicInfo();  //设置任务的基本信息
						  // 显示插件信息的列表框控件
	CComboBox m_pluginslist;
	virtual BOOL OnInitDialog();
	afx_msg void OnBnClickedOnExcutePlugings();
};
