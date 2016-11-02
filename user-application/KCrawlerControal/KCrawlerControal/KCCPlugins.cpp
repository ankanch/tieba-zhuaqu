// KCCPlugins.cpp : 实现文件
//

#include "stdafx.h"
#include "KCrawlerControal.h"
#include "KCCPlugins.h"
#include "afxdialogex.h"
#include <locale.h>


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
	char* old_locale = _strdup(setlocale(LC_CTYPE, NULL));
	setlocale(LC_CTYPE, "chs");//设定<ctpye.h>中字符处理方式
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
	setlocale(LC_CTYPE, old_locale);
	free(old_locale);//还原区域设定
	cfg.Close();
}

void KCCPlugins::setupBasicInfo()
{

}



BEGIN_MESSAGE_MAP(KCCPlugins, CDialogEx)
	ON_BN_CLICKED(IDC_ON_EXCUTE_PLUGINGS, &KCCPlugins::OnBnClickedOnExcutePlugings)
END_MESSAGE_MAP()


// KCCPlugins 消息处理程序


BOOL KCCPlugins::OnInitDialog()
{
	CDialogEx::OnInitDialog();

	// TODO:  在此添加额外的初始化
	setupBasicInfo();
	loadPlugins();

	return TRUE;  // return TRUE unless you set the focus to a control
				  // 异常: OCX 属性页应返回 FALSE
}


void KCCPlugins::OnBnClickedOnExcutePlugings()
{
	// TODO: 在此添加控件通知处理程序代码
	//判断选择项
	int selected = m_pluginslist.GetCurSel();
	if (selected < 0)
	{
		MessageBox(_T("未选中任何可用插件！"), _T("错误"), MB_ICONERROR | MB_OK);
		return;
	}
	CString exefilename = pluginlist[selected].exefilename;
	TCHAR currentDir[MAX_PATH];
	GetCurrentDirectory(MAX_PATH,currentDir);
	CString dir = currentDir;
	exefilename = _T("/C python " + dir + "\\plugins\\") + exefilename;
	//调用python脚本
	ShellExecute(NULL, _T("open"),_T("cmd.exe"), exefilename, NULL, SW_SHOW);
}
