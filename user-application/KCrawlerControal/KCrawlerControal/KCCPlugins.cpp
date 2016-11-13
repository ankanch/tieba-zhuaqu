// KCCPlugins.cpp : 实现文件
//

#include "stdafx.h"
#include "KCrawlerControal.h"
#include "KCCPlugins.h"
#include "afxdialogex.h"
#include <locale.h>
#include "KCrawlerControalDlg.h"


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

//该函数为老版插件搜索函数，已经被弃用，将会在未来的版本更新中消失。
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

CString KCCPlugins::SearchPlugs()
{
	CFileFind finder;
	BOOL bWorking = finder.FindFile(_T(".\\plugins\\*.*"));
	CString pluginsData;
	while (bWorking)
	{
		bWorking = finder.FindNextFile();
		if (finder.IsDots())
			continue;
		CString foldername = (LPCTSTR)finder.GetFileName();
		//MessageBox(foldername);
		//理论上讲插件都在文件夹里面，所以，这里我们要判断是不是文件夹
		if (finder.IsDirectory())
		{
			//MessageBox(_T("搜索main.py"), _T("发现目录..."), MB_ICONINFORMATION);
			CFileFind findmain;
			CString mainpath = _T(".\\plugins\\") + foldername + _T("\\main.py");
			if (findmain.FindFile(mainpath))
			{
				//读取插件信息，插件信息由以下3个字段定义，定义在main.py文件里面
				//KCC_PLUGIN_NAME：定义了插件名字
				//KCC_PLUGIN_DESCRIPTION：定义了插件描述
				//KCC_PLUGIN_COPYRIGHT：定义了插件作者以及版权信息
				CStdioFile readinfo;
				readinfo.Open(mainpath, CFile::modeRead);
				//MessageBox(_T("XXXXXXXXXXXXXXXXXXXX"), _T("找到可用插件"), MB_ICONINFORMATION);
				CString line;
				CString NAME = foldername, DES = _T(""), CR=_T("未知作者");
				int findcount = 0;
				while (readinfo.ReadString(line))
				{
					CKCCDlg kccdlg;
					line = kccdlg.UTF8_TO_GBK((char*)line.GetBuffer(0));
					if (findcount == 3)
					{
						break;
					}
					if (line.Find(_T("KCC_PLUGIN_NAME")) >= 0)
					{
						NAME = line.Right(line.GetLength() - line.Find(_T("=")) - 1);
						findcount++;
					}
					if (line.Find(_T("KCC_PLUGIN_DESCRIPTION")) >= 0)
					{
						DES = line.Right(line.GetLength() - line.Find(_T("=")) - 1);
						findcount++;
					}
					if (line.Find(_T("KCC_PLUGIN_COPYRIGHT")) >= 0)
					{
						CR = line.Right(line.GetLength() - line.Find(_T("=")) - 1);
						findcount++;
					}
				}
				pluginsData += NAME + _T("=") + DES + _T("=") + CR + _T("=") + foldername + _T("\\main.py#");
				readinfo.Close();
			}
		}
	}

	//插件搜索完毕，信息都储存在pluginsData中
	return pluginsData;
}

void KCCPlugins::LoadPluginsNV()
{
	CString pluginsData = SearchPlugs();
	///MessageBox(pluginsData);
	int pluginscount = 0;
	for (int i = 0; i < pluginsData.GetLength(); i++)
	{
		if (pluginsData[i] == CString(_T("#")))
		{
			pluginscount++;
		}
	}
	pluginlist = new Plugin[pluginscount];
	for (int i = 0; i < pluginscount; i++)
	{
		CString NAME, DES, CP, PATH;
		NAME = pluginsData.Left(pluginsData.Find(_T("=")));
		pluginsData = pluginsData.Right(pluginsData.GetLength() - pluginsData.Find(_T("=")) - 1);
		DES = pluginsData.Left(pluginsData.Find(_T("=")));
		pluginsData = pluginsData.Right(pluginsData.GetLength() - pluginsData.Find(_T("=")) - 1);
		CP = pluginsData.Left(pluginsData.Find(_T("=")));
		pluginsData = pluginsData.Right(pluginsData.GetLength() - pluginsData.Find(_T("=")) - 1);
		PATH = pluginsData.Left(pluginsData.Find(_T("#")));
		pluginsData = pluginsData.Right(pluginsData.GetLength() - pluginsData.Find(_T("#")) - 1);
		//保存信息到数组中方便执行
		pluginlist[i].name = NAME;
		pluginlist[i].descri = DES;
		pluginlist[i].exefilename = PATH;
		//添加到列表框中
		CString liststr = NAME + _T("->") + DES;
		m_pluginslist.AddString(liststr);
	}


}



BEGIN_MESSAGE_MAP(KCCPlugins, CDialogEx)
	ON_BN_CLICKED(IDC_ON_EXCUTE_PLUGINGS, &KCCPlugins::OnBnClickedOnExcutePlugings)
END_MESSAGE_MAP()


// KCCPlugins 消息处理程序


BOOL KCCPlugins::OnInitDialog()
{
	CDialogEx::OnInitDialog();

	// TODO:  在此添加额外的初始化
	LoadPluginsNV();
	setupBasicInfo();

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
