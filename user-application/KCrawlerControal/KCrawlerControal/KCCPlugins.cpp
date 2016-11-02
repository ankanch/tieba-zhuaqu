// KCCPlugins.cpp : 实现文件
//

#include "stdafx.h"
#include "KCrawlerControal.h"
#include "KCCPlugins.h"
#include "afxdialogex.h"


// KCCPlugins 对话框

IMPLEMENT_DYNAMIC(KCCPlugins, CDialogEx)

KCCPlugins::KCCPlugins(CWnd* pParent /*=NULL*/)
	: CDialogEx(IDD_DIALOG_USE_PLUGINS, pParent)
{

}

KCCPlugins::~KCCPlugins()
{
	delete[] pluginlist;
}

void KCCPlugins::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
	DDX_Control(pDX, IDC_COMBO2, m_pluginslist);
}

void KCCPlugins::loadPlugins()
{
	CStdioFile cfg;
	cfg.Open(PATH_PLUGINS_INDEX_FILE, CFile::modeRead);
	CString line = _T("");
	int pluginscount = 0;
	//插件计数
	while (cfg.ReadString(line))
	{
		//行组成：KCCPLUGINS=插件名=插件简介=插件文件名
		if (line.Find(_T("KCCPLUGINS")) >= 0)
		{
			pluginscount++;
		}
		line = _T("");
	}
	if (pluginscount < 1)
	{
		MessageBox(_T("未找到任何可用插件！你可能无法进行任何数据分析操作。"), _T("错误"), MB_ICONERROR | MB_OK);
		cfg.Close();
		return;
	}
	cfg.SeekToBegin();
	pluginlist = new Plugin[pluginscount];
	//循环加载插件
	int i = 0;
	while (cfg.ReadString(line))
	{
		//插件索引结构：每一行代表一个插件
		//行组成：KCCPLUGINS=插件名=插件简介=插件文件名
		if (line.Find(_T("KCCPLUGINS")) >= 0)
		{
			line = line.Right(line.GetLength() - line.Find(_T("=")) - 1);
			CString name = line.Left(line.Find(_T("=")));
			line = line.Right(line.GetLength() - line.Find(_T("=")) - 1);
			CString descri = line.Left(line.Find(_T("=")));
			line = line.Right(line.GetLength() - line.Find(_T("=")) - 1);
			CString exefilename = line;
			if (exefilename.GetLength() < 3 || name.GetLength() == 0)
			{
				continue;
			}
			CString liststr = name + _T("->") + descri;
			m_pluginslist.AddString(liststr);
			//保存插件信息到一个表中方便执行
			pluginlist[i].name = name;
			pluginlist[i].descri = descri;
			pluginlist[i].exefilename = exefilename;
			i++;
		}
		line = _T("");
	}
	cfg.Close();
}


BEGIN_MESSAGE_MAP(KCCPlugins, CDialogEx)
END_MESSAGE_MAP()


// KCCPlugins 消息处理程序


BOOL KCCPlugins::OnInitDialog()
{
	CDialogEx::OnInitDialog();

	// TODO:  在此添加额外的初始化
	loadPlugins();

	return TRUE;  // return TRUE unless you set the focus to a control
				  // 异常: OCX 属性页应返回 FALSE
}
