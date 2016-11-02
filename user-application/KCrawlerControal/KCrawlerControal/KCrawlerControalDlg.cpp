
// KCrawlerControalDlg.cpp : 实现文件
//

#include "stdafx.h"
#include "KCrawlerControal.h"
#include "KCrawlerControalDlg.h"
#include "afxdialogex.h"
#include "CreateJobDlg.h"
#include "KCCPlugins.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif


// 用于应用程序“关于”菜单项的 CAboutDlg 对话框

class CAboutDlg : public CDialogEx
{
public:
	CAboutDlg();

// 对话框数据
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_ABOUTBOX };
#endif

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV 支持

// 实现
protected:
	DECLARE_MESSAGE_MAP()
};

CAboutDlg::CAboutDlg() : CDialogEx(IDD_ABOUTBOX)
{
}

void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialogEx)
END_MESSAGE_MAP()


// CKCCDlg 对话框



CKCCDlg::CKCCDlg(CWnd* pParent /*=NULL*/)
	: CDialogEx(IDD_KCRAWLERCONTROAL_DIALOG, pParent)
{
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void CKCCDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
	DDX_Control(pDX, IDC_EDIT_LOG, m_edit_log);
	DDX_Control(pDX, IDC_LIST_CRAWLERLIST, m_liat_crawlerlist);
}

BEGIN_MESSAGE_MAP(CKCCDlg, CDialogEx)
	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	ON_BN_CLICKED(IDC_BUTTON_CREATEJOB, &CKCCDlg::OnBnClickedButtonCreatejob)
	ON_MESSAGE(WM_UPDATE_CRAWLER_LIST,onLoadCrawlerList)
	ON_MESSAGE(WM_DOWNLOAD_RESULT,onDownloadResultMsg)
	ON_BN_CLICKED(IDC_BUTTON_DOWNLOAD_RESULT_FILE, &CKCCDlg::OnBnClickedButtonDownloadResultFile)
	ON_BN_CLICKED(IDC_BUTTON_LOADANALY, &CKCCDlg::OnBnClickedButtonLoadanaly)
END_MESSAGE_MAP()


// CKCCDlg 消息处理程序

BOOL CKCCDlg::OnInitDialog()
{
	CDialogEx::OnInitDialog();

	// 将“关于...”菜单项添加到系统菜单中。

	// IDM_ABOUTBOX 必须在系统命令范围内。
	ASSERT((IDM_ABOUTBOX & 0xFFF0) == IDM_ABOUTBOX);
	ASSERT(IDM_ABOUTBOX < 0xF000);

	CMenu* pSysMenu = GetSystemMenu(FALSE);
	if (pSysMenu != NULL)
	{
		BOOL bNameValid;
		CString strAboutMenu;
		bNameValid = strAboutMenu.LoadString(IDS_ABOUTBOX);
		ASSERT(bNameValid);
		if (!strAboutMenu.IsEmpty())
		{
			pSysMenu->AppendMenu(MF_SEPARATOR);
			pSysMenu->AppendMenu(MF_STRING, IDM_ABOUTBOX, strAboutMenu);
		}
	}

	// 设置此对话框的图标。  当应用程序主窗口不是对话框时，框架将自动
	//  执行此操作
	SetIcon(m_hIcon, TRUE);			// 设置大图标
	SetIcon(m_hIcon, FALSE);		// 设置小图标

	AfxSocketInit();
	firstrun = true;
	// TODO: 在此添加额外的初始化代码
	loadConfig();
	InitEnvirment();
	LoadCrawlerList();
	//循环加载爬虫列表
	AfxBeginThread(LoopLoadCrawlerList, AfxGetMainWnd()->m_hWnd);

	return TRUE;  // 除非将焦点设置到控件，否则返回 TRUE
}

int CKCCDlg::DATA_REFRESH_RATE = 5;

void CKCCDlg::OnSysCommand(UINT nID, LPARAM lParam)
{
	if ((nID & 0xFFF0) == IDM_ABOUTBOX)
	{
		CAboutDlg dlgAbout;
		dlgAbout.DoModal();
	}
	else
	{
		CDialogEx::OnSysCommand(nID, lParam);
	}
}

// 如果向对话框添加最小化按钮，则需要下面的代码
//  来绘制该图标。  对于使用文档/视图模型的 MFC 应用程序，
//  这将由框架自动完成。

void CKCCDlg::OnPaint()
{
	if (IsIconic())
	{
		CPaintDC dc(this); // 用于绘制的设备上下文

		SendMessage(WM_ICONERASEBKGND, reinterpret_cast<WPARAM>(dc.GetSafeHdc()), 0);

		// 使图标在工作区矩形中居中
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;

		// 绘制图标
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CDialogEx::OnPaint();
	}
}

//当用户拖动最小化窗口时系统调用此函数取得光标
//显示。
HCURSOR CKCCDlg::OnQueryDragIcon()
{
	return static_cast<HCURSOR>(m_hIcon);
}



void CKCCDlg::OnBnClickedButtonCreatejob()
{
	// TODO: 在此添加控件通知处理程序代码
	CCreateJobDlg CCD;
	JobCreateData JCD;
	CCD.tiebaName = _T("成都信息工程大学");
	CCD.pages = 0;
	CCD.DoModal();
	JCD.tiebaName = CCD.tiebaName;
	JCD.pages = CCD.pages;
	if (!KCCCreateJob(JCD))
	{
		KCCLog(_T(">>>>>任务创建失败！\n"));
	}
	else
	{
		KCCLog(_T(">>>>>任务创建成功！\n"));
	}
}

LRESULT  CKCCDlg::onLoadCrawlerList(WPARAM WP, LPARAM LP)
{
	if (DEBUG_MODE)
	{
		return 0;
	}
	LoadCrawlerList();
	return 0;
}

LRESULT CKCCDlg::onDownloadResultMsg(WPARAM WP, LPARAM LP)
{
	CSocket s;
	s.Socket();
	if (!s.Connect(DATA_SERVER_IP, DATA_SERVER_PORT))
	{
		KCCLog(_T("错误：无法连接到TaskManager服务器！请检查你的网络连接后重试！"));
		return 0;
	}
	KCCLog(_T("连接中..."));
	CString RESULT_TRANSFER_CMD = _T("304,REQUEST FOR JOB RESULT");
	USES_CONVERSION;
	char *cmdbuf = T2A(RESULT_TRANSFER_CMD);
	cmdbuf = UnicodeToUTF8(RESULT_TRANSFER_CMD.GetBuffer(0));
	s.Send(cmdbuf, strlen(cmdbuf));
	KCCLog(_T("请求已发送，等待TaskManager服务器响应..."));
	CString cp;
	char recvBuf[1024] = { 0 };
	s.Receive((void *)recvBuf, 1024);
	cp = UTF8_TO_GBK(recvBuf);
	KCCLog(_T("TaskManager:" + cp));
	//开始接收文件
	//首先得到文件大小
	memset(recvBuf, 0, sizeof(char) * 1024);
	s.Receive((void *)recvBuf, 1024);
	cp = UTF8_TO_GBK(recvBuf);
	KCCLog(_T("TaskManager:->result file size:" + cp));
	int filesize = _ttoi(cp);
	//然后开始接收
	CString filedata = _T("");
	int recivedsize = 0;
	KCCLog(_T("下载中...."));
	CFile re;
	re.Open(_T("result"), CFile::modeCreate | CFile::modeWrite | CFile::typeBinary);
	while (recivedsize < filesize)
	{
		memset(recvBuf, 0, sizeof(char) * 1024);
		int rs = s.Receive((void *)recvBuf, 1024);
		re.Write(recvBuf,rs);
		cp = UTF8_TO_GBK(recvBuf);
		filedata += cp;
		recivedsize += rs;
	}
	KCCLog(_T("任务结果下载完毕！"));
	s.Close();
	re.Close();
	return 0;
}

void CKCCDlg::loadConfig()
{
	CStdioFile cfg;
	cfg.Open(PATH_CONFIG_FILE,CFile::modeRead);
	CString line = _T("");
	while (cfg.ReadString(line))
	{
		//MessageBox(line);
		if(line.Find(_T("SERVER_HOST")) >= 0){
			//读取服务器地址
			DATA_SERVER_IP = line.Right(line.GetLength() - line.Find(_T("=")) - 1);
		}
		else if(line.Find(_T("SERVER_PORT")) >= 0) {
			//读取端口
			DATA_SERVER_PORT = _ttoi(line.Right(line.GetLength() - line.Find(_T("=")) - 1));
			if (DATA_SERVER_PORT > 65536)
			{
				DATA_SERVER_PORT = 50005;
			}
		}
		else if(line.Find(_T("REFRESH_RATE")) >= 0) {
			//读取更新爬虫列表频率
			DATA_REFRESH_RATE = _ttoi(line.Right(line.GetLength() - line.Find(_T("=")) - 1));
			if (DATA_REFRESH_RATE < 3)
			{
				DATA_REFRESH_RATE = 5;
			}
		}
		else if(line.Find(_T("MODE_DEBUG")) >= 0) {
			//是否开启调试模式
			if (line.Right(line.GetLength() - line.Find(_T("=")) - 1) == _T("TRUE"))
			{
				DEBUG_MODE = true;
			}
		}
		line = _T("");
	}
	cfg.Close();
}


void CKCCDlg::KCCLog(const CString logdata)
{
	m_edit_log.SetSel(m_edit_log.GetSel());
	m_edit_log.ReplaceSel(_T(">>>>>"+ logdata +"\n"));
	m_edit_log.LineScroll(m_edit_log.GetLineCount());
}

const bool CKCCDlg::KCCCreateJob(const JobCreateData jcd)
{
	KCCLog(_T("初始化..."));
	CSocket s;
	s.Socket();
	if (!s.Connect(DATA_SERVER_IP, DATA_SERVER_PORT))
	{
		KCCLog(_T("错误：无法连接到TaskManager服务器！请检查你的网络连接后重试！"));
		return false;
	}
	KCCLog(_T("发送任务清单..."));
	CString JOB_CREATE_CMD = _T("303,TEST,");
	CString cp;
	//一次任务清单发送
	cp.Format(_T("%d"), jcd.pages);
	JOB_CREATE_CMD += (jcd.tiebaName + _T(",") + cp);
	USES_CONVERSION;
	char *cmdbuf = T2A(JOB_CREATE_CMD);
	cmdbuf = UnicodeToUTF8(JOB_CREATE_CMD.GetBuffer(0));
	s.Send(cmdbuf, strlen(cmdbuf));
	KCCLog(_T("任务清单发送完毕，等待TaskManager服务器响应..."));
	char recvBuf[1024] = { 0 };
	s.Receive((void *)recvBuf, 1024);
	cp = UTF8_TO_GBK(recvBuf);
	KCCLog(_T("TaskManager:" + cp));
	//二次确认
	JOB_CREATE_CMD = _T("666,JOB COMFIRM");
	KCCLog(_T("确认任务中..."));
	cmdbuf = UnicodeToUTF8(JOB_CREATE_CMD.GetBuffer(0));
	s.Send(cmdbuf, strlen(cmdbuf));
	s.Receive((void *)recvBuf, 1024);
	cp = UTF8_TO_GBK(recvBuf);
	KCCLog(_T("TaskManager:" + cp));

	s.Close();
	return true;
}

void CKCCDlg::InitEnvirment()
{
	//初始化爬虫列表控件
	//包括： 爬虫ID，IP地址，端口，工作状态，上线时间
	int size[10] = { 50,220,80,80,120 };
	CString name[10] = { _T("ID") ,_T("IP地址") ,_T("端口") ,_T("工作状态") ,_T("上线时间") };
	for (int i = 0; i < 5; i++)
	{
		m_liat_crawlerlist.InsertColumn(i, (LPWSTR)(LPCTSTR)name[i], LVCFMT_CENTER, size[i]);
	}
	
}

void  CKCCDlg::LoadCrawlerList()
{
	CSocket s;
	s.Socket();
	char recvBuf[1024] = { 0 };
	if (firstrun)
	{
		KCCLog(_T("加载爬虫列表..."));
	}
	if (!s.Connect(DATA_SERVER_IP, DATA_SERVER_PORT))
	{
		KCCLog(_T("错误：无法刷新爬虫列表->无法连接到TaskManager服务器->请检查你的网络连接后重试！"));
		return ;
	}
	//去掉服务器的欢迎信息
	s.Receive((void *)recvBuf, 1024);
	CString REQUEST_CRAWLER_LIST = _T("302,request for crawler list");
	CString cp;
	USES_CONVERSION;
	//发送命令
	char *cmdbuf = T2A(REQUEST_CRAWLER_LIST);
	s.Send(cmdbuf, strlen(cmdbuf));
	memset(recvBuf, 0, sizeof(char) * 1024);
	s.Receive(recvBuf, 1024);
	s.Close();
	cp = UTF8_TO_GBK(recvBuf);
	if (firstrun)
	{
		KCCLog(_T("TaskManager:" + cp));
		KCCLog(_T("爬虫列表加载完成！"));
	}
	//向ListControl中加载爬虫列表
	cp = cp.Right(cp.GetLength() - cp.Find(',') - 1);
	cp = cp.Left(cp.Find(','));
	//MessageBox(cp);
	int lastat = 0;
	int online = 0;
	m_liat_crawlerlist.DeleteAllItems();
	while (cp.GetLength() > 0)
	{
		lastat = cp.Find('@');
		CString ID = cp.Left(cp.Find('@'));
		cp = cp.Right(cp.GetLength() - cp.Find('@') - 1);
		CString IP = cp.Left(cp.Find('@'));
		cp = cp.Right(cp.GetLength() - cp.Find('@') - 1);
		CString PORT = cp.Left(cp.Find('@'));
		cp = cp.Right(cp.GetLength() - cp.Find('@') - 1);
		//MessageBox(cp);
		if (ID == "" || ID == " ")
		{
			continue;
		}
		m_liat_crawlerlist.InsertItem(online,ID);
		m_liat_crawlerlist.SetItemText(online, 1, IP);
		m_liat_crawlerlist.SetItemText(online, 2, PORT);
		m_liat_crawlerlist.SetItemText(online, 3, _T("N/A"));
		m_liat_crawlerlist.SetItemText(online, 4, _T("N/A"));
		online++;
		if (cp.Find('@') < 0)
		{
			break;
		}
	}
	cp.Format(_T("%d"), online);
	SetDlgItemText(IDC_STATIC_CRAWLERSUM, cp);
	firstrun = false;
}

UINT  CKCCDlg::LoopLoadCrawlerList(LPVOID pParam)
{
	HWND TH = (HWND)pParam;
	if (TH == nullptr)
	{
		return -1;  //-1 = 空指针
	}
 	while (true)
	{
		Sleep(1000*DATA_REFRESH_RATE);
		::PostMessage(TH,WM_UPDATE_CRAWLER_LIST,NULL,NULL);
	}
	return 0;
}

UINT  CKCCDlg::DownloadResultNewThread(LPVOID pParam)
{
	HWND TH = (HWND)pParam;
	if (TH == nullptr)
	{
		return -1;  //-1 = 空指针
	}
	::PostMessage(TH, WM_DOWNLOAD_RESULT, NULL, NULL);
	return 0;
}

const wchar_t*  CKCCDlg::UTF8_TO_GBK(const char* str)
{//
	int    textlen = 0;
	wchar_t * result;
	textlen = MultiByteToWideChar(CP_UTF8, 0, str, -1, NULL, 0);
	result = (wchar_t *)malloc((textlen + 1) * sizeof(wchar_t));
	memset(result, 0, (textlen + 1) * sizeof(wchar_t));
	MultiByteToWideChar(CP_UTF8, 0, str, -1, (LPWSTR)result, textlen);
	return    result;
}

char * CKCCDlg::UnicodeToUTF8(const wchar_t *str)
{
	char * result;
	int textlen = 0;
	// wide char to multi char
	textlen = WideCharToMultiByte(CP_UTF8, 0, str, -1, NULL, 0, NULL, NULL);
	result = (char *)malloc((textlen + 1) * sizeof(char));
	memset(result, 0, sizeof(char) * (textlen + 1));
	WideCharToMultiByte(CP_UTF8, 0, str, -1, result, textlen, NULL, NULL);
	return result;
}


void CKCCDlg::OnBnClickedButtonDownloadResultFile()
{
	AfxBeginThread(DownloadResultNewThread, AfxGetMainWnd()->m_hWnd);
}


void CKCCDlg::OnBnClickedButtonLoadanaly()
{
	// TODO: 在此添加控件通知处理程序代码
	KCCPlugins kccp;
	kccp.DoModal();
}
