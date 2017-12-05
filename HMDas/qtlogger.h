#ifndef QTLOGGER_H
#define QTLOGGER_H

#include <QObject>
#include <QThread>
#include <QFile>
#include <QDateTime>
//#include <qlogging.h>

class QtLogger;

class LoggerWriter
	: public QObject
{
	Q_OBJECT

public:
	LoggerWriter()
		:m_cDate(QDateTime::currentDateTime())
	{

	}
	QFile m_File;
	QDateTime m_cDate;
	QtLogger* m_ptCaller;

public:

	void setCaller(QtLogger* ptCaller)
	{
		m_ptCaller = ptCaller;
	}

	QtLogger* getCaller()
	{
		return m_ptCaller;
	}

public slots:

	void on_toLogger(int nType,const QString& strlog);

	void on_toQuit()
	{
		if(m_File.isOpen())
		{
			m_File.close();
		}
	}
};


class QtLogger 
	: public QObject
{
	Q_OBJECT

	QThread loggerThread;

public:

	QtLogger(QObject *parent = 0);

	~QtLogger();

	static QtLogger* getLogger();

	void InitLogger(int nType = QtDebugMsg);

	int GetLogType()
	{
		return m_nLogType;
	}


private:

	LoggerWriter m_cWriter;
	static QtLogger* m_pLogger;
	int m_nLogType;
	
	
public slots:


signals :
	void evt_rawLog(int nType, const QString& strMsg);
	void evt_toLogger(int nType,const QString& strMsg);

public:
	// 日志回调函数
	static void loghanderCallback(QtMsgType type, const QMessageLogContext &context,const QString & msg);
	
};

#endif // QTLOGGER_H
