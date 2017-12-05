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
		station = "SCN";//�����
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
	//�شŲ���ƫ��ͼ����
	int frontindex;
	int backindex;
	//�ص���
	int overlines;
	QString triggerselect;
	//���ݻ�������С
	int buffsize;
	//��ɫͼ��0�ڰ�1��ɫ
	int colorformt;

	//�豸��
	QString devicecode;
	//�豸λ��
	QString locatecode;
	//վ��
	QString station;
	//ʶ��udp���Ͷ˿�
	int SEND_REGN_U_Port;
	int nExpPlus;  // �ع�����

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
	//ͼƬ�����Ŀ¼
	QString m_szSavePath;
	//������ip��ַ
	QString serverip;
	//���ȷ���TCP�˿ڣ���������Ϣ������Ϣ
	int Server_T_Port;
	//���ܿ���udp���Ͷ˿�
	int Recv_CTRL_U_Port;

	//ʶ��udp���ܶ˿�
	int RECV_REGN_U_Port;
	//������ʽ
	int nAxiskind;
	//ϵͳ��������
	unsigned long carindex;
	//cfgpath;
	QString m_cfgpath;
	//����LE/TE
	QString m_TrainType;

	QString m_strPos;	
	QString m_strTitle;
	QString m_strLastUUID;
	int m_nSaveDays;  // �ɼ��������������
	int m_nAutoMode;
	int m_nFpsNormal;
	int m_nFpsStop;
	int m_nAutoReboot;  // ��������쳣ʱ �Զ�����
	int dropPresave;
	int m_nNeedAxis;   // �Ƿ���Ҫ����Ϣ
	int m_nSaveMode;   // ���淽ʽ ����������  ���� ���� 0/1�߼���ʽ
	// ��󱣴�����
	long nMaxSaveCnt;
};

