#pragma once
#include <QString>
#include <vector>

struct CameraCfg
{
	CameraCfg()
	{
		id = "CameraID";
		channel = "new channel";
		x = y = height = width = 0;
		triggersrc = "software";
		triggermode = "false";
		exposuremode = "timed";
		exposuretime = 20;
		gain = -24;
		compressnum = 2;
		queuesize = 1000;
		iszoom = false;
		percent = 50;
		iscut = false;
		cx = cy = 0;
		cw = ch = 100;
		cutmode = "both";
		istransform = false;
		isrotation = false;
		rotationmode = 0;
		frontindex = 0;
		backindex = 0;
		overlines = 0;
		triggerselect = "";
		buffsize = 10;
		exposureauto = "off";
		avgmax = avgmin = 0;
		colorformt = 0;

		devicecode = "CH";
		locatecode = "00";
		station = "SCN";//神池南
	}
	QString id;
	QString channel;
	int x;
	int y;
	int width;
	int height;
	QString triggersrc;
	QString triggermode;
	QString exposuremode;
	double exposuretime;
	QString exposureauto;
	int avgmax;
	int avgmin;
	int gain;
	int compressnum;
	int queuesize;
	bool iszoom;
	int percent;
	bool iscut;
	int cx;
	int cy;
	int cw;
	int ch;
	QString cutmode;
	bool istransform;
	bool isrotation;
	int rotationmode;
	//地磁侧向偏移图像数
	int frontindex;
	int backindex;
	//重叠数
	int overlines;
	QString triggerselect;
	//数据缓冲区大小
	int buffsize;
	//彩色图像0黑白1彩色
	int colorformt;

	//设备码
	QString devicecode;
	//设备位置
	QString locatecode;
	//站点
	QString station;
	//识别udp发送端口
	int SEND_REGN_U_Port;
	int nExpPlus;  // 曝光增量

};


class CHMConfig
{

public:
	static CHMConfig *Instance();

	CHMConfig();
	~CHMConfig();

	bool load(QString path);
	void save();

public:

protected:
	std::vector<CameraCfg> m_cameravec;
	//图片保存根目录
	QString m_szSavePath;
	//服务器ip地址
	QString serverip;
	//调度服务TCP端口，发送轴信息车次信息
	int Server_T_Port;
	//接受控制udp发送端口
	int Recv_CTRL_U_Port;

	//识别udp接受端口
	int RECV_REGN_U_Port;
	//反馈方式
	int nAxiskind;
	//系统过车次数
	unsigned long carindex;
	//cfgpath;
	QString m_cfgpath;
	//车型LE/TE
	QString m_TrainType;

	QString m_strPos;	
	QString m_strTitle;
	QString m_strLastUUID;
	int m_nSaveDays;  // 采集保存多少天数据
	int m_nAutoMode;
	int m_nFpsNormal;
	int m_nFpsStop;
	int m_nAutoReboot;  // 相机连接异常时 自动重启
	int dropPresave;
	int m_nNeedAxis;   // 是否需要轴消息
	int m_nSaveMode;   // 保存方式 按照年月日  还是 按照 0/1逻辑方式
	// 最大保存张数
	long nMaxSaveCnt;
};

