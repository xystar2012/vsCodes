#include "HMConfig.h"
#include <QSettings>
#include <QFile>
#include <QDebug>

static QString g_strConfigPath = "config.ini";


#pragma execution_character_set("utf-8")


CHMConfig::CHMConfig()
{

}

CHMConfig::~CHMConfig()
{
	
}

bool CHMConfig::load(QString qPath)
{
	if (!QFile(qPath).exists())
	{
		qDebug() << "configFile:" << qPath << " not exist ...";
		
		return false;
	}

	QSettings iniFile(qPath, QSettings::IniFormat);
	iniFile.setIniCodec("utf-8");

	iniFile.beginGroup("BASEINFO");

	int nCams = iniFile.value(("count"), 0).toInt();
	m_szSavePath = iniFile.value("SAVEPATH", "d:/data/").toString();
	serverip = iniFile.value("SERVERIP", "127.0.0.1").toString();
		
	Server_T_Port = iniFile.value("SERVERPORT", "50000").toInt();
	Recv_CTRL_U_Port = iniFile.value("CTRLPORT", "30000").toInt();
	RECV_REGN_U_Port =iniFile.value("RECVREGNPORT", "30002").toInt();
	nAxiskind = iniFile.value("AXIS", "0").toInt();

	m_TrainType = iniFile.value("TRAINTYPE", "LE").toString();
	m_strPos = iniFile.value("POS", "1").toString();  // 位置 0  1
	m_strTitle = iniFile.value("DLGTITLE", "华眸采集软件").toString();  // 位置 0  1
	m_nSaveDays = iniFile.value(("SAVEDAYS"), 300).toInt();
	m_nAutoMode = iniFile.value(("AUTOMODE"), 1).toInt();  // 0 -- auto 曝光 
	m_nFpsNormal = iniFile.value(("FPS_NORMAL")).toInt();  // 正常征率
	m_nFpsStop = iniFile.value(("FPS_STOP"), 3).toInt();  // 停车帧率
	// 设置参数异常时 是否重启
	m_nAutoReboot = iniFile.value(("TOREBOOT"), 1).toInt();  // 停车帧率
	this->dropPresave = iniFile.value(("DROPPREPIC"), 1).toInt();
	// 最大保存图片上限
	nMaxSaveCnt = iniFile.value("MAXSAVECOUNT", "3000").toInt();
	m_nNeedAxis = iniFile.value(("NEEDAXIS"), 1).toInt();;  // 停车帧率
	m_nSaveMode = iniFile.value(("SAVE_TE"), 0).toInt();;  // TE存图方式


	iniFile.endGroup();
	
	for (int i = 0; i < nCams; i++)
	{
		CameraCfg cameraobj;

		iniFile.beginGroup(QString("CAMERA%1").arg(i));
		cameraobj.id = iniFile.value("ID", "S1").toString();
		cameraobj.channel = iniFile.value(("CHANNEL"), "1").toInt();
		iniFile.value(("X"), 0).toInt();
		iniFile.value(("Y"), 0).toInt();
		iniFile.value(("WIDTH"), 0).toInt();
		iniFile.value(("HEIGHT"), 0).toInt();
		cameraobj.iszoom = iniFile.value(("ZOOM"), 0).toBool();
		cameraobj.percent = iniFile.value(("PERCENT"), 0).toInt();
		cameraobj.frontindex = iniFile.value(("FRONTINDEX"), 0).toInt();
		cameraobj.backindex = iniFile.value(("BACKINDEX"), 0).toInt();
		cameraobj.istransform = iniFile.value(("TRANSFORM"), 0).toBool();
		cameraobj.isrotation = iniFile.value("ROTATION", 0).toBool();
		cameraobj.rotationmode = iniFile.value(("ROTATIONMODE"), 0).toInt();
		cameraobj.iscut = iniFile.value(("CUT"), 0).toBool();
		cameraobj.cutmode = iniFile.value(("CUTMODE"), "both").toString();
		cameraobj.cx = iniFile.value(("CX"), 0).toInt();
		cameraobj.cy = iniFile.value(("CY"), 0).toInt();
		cameraobj.cw = iniFile.value(("CW"), 0).toInt();
		cameraobj.ch = iniFile.value(("CH"), 0).toInt();

		cameraobj.triggermode = iniFile.value(("TRIGGERMODE"), "true").toString();
		cameraobj.triggersrc = iniFile.value(("TRIGGERSRC"), "line0").toString();
		cameraobj.exposuremode = iniFile.value(("EXPOSUREMODE"), "timed").toString();
		cameraobj.exposureauto = iniFile.value(("EXPOSUREAUTO"), "off").toString();
		cameraobj.triggerselect = iniFile.value(("TRIGGERSELECT"), "framestart").toString();
		cameraobj.colorformt = iniFile.value(("COLORFORMAT"), 0).toInt();
		cameraobj.exposuretime = iniFile.value(("EXPOSURETIME"), 0).toDouble();
		cameraobj.gain = iniFile.value(("GAIN"), 0).toDouble();

		cameraobj.avgmax = iniFile.value(("AVGMAX"), 200).toInt();
		cameraobj.avgmin = iniFile.value(("AVGMIN"), 150).toInt();

		// DATA SIZE
		cameraobj.compressnum = iniFile.value(("COMPRESSNUM"), 1).toInt();
		cameraobj.queuesize = iniFile.value(("QUEUESIZE"), 100).toInt();
		cameraobj.buffsize = iniFile.value(("BUFFERSIZE"), 10).toInt();
		
		cameraobj.devicecode = iniFile.value(("DEVICECODE"), "CH").toString();
		cameraobj.locatecode = iniFile.value(("LOCATECODE"), "CH").toString();
		cameraobj.station = iniFile.value(("STATION"), "SCN").toString();

		cameraobj.nExpPlus = iniFile.value(("EXP_PLUS"), 300).toInt();  // 曝光增量
		m_cameravec.push_back(cameraobj);

		iniFile.endGroup();
	}

	return true;
}

void CHMConfig::save()
{

}

CHMConfig * CHMConfig::Instance()
{
	static CHMConfig g_Cfg;

	return &g_Cfg;
}
