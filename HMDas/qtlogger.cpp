#include "qtlogger.h"
#include <QDir>
#include <QTextStream>
#include <QCoreApplication>
#include <QDebug>

QtLogger::QtLogger(QObject *parent)
	: QObject(parent)
{
	m_cWriter.setCaller(this);

	connect(this,&QtLogger::evt_toLogger,&m_cWriter,&LoggerWriter::on_toLogger);
	connect(&loggerThread,&QThread::quit,&m_cWriter,&LoggerWriter::on_toQuit);
	
	m_cWriter.moveToThread(&loggerThread);

	loggerThread.start();
}

QtLogger::~QtLogger()
{
	loggerThread.quit();
	loggerThread.wait(300);
}


QtLogger* QtLogger::getLogger()
{
	static QtLogger onlyOneLogger;

	return &onlyOneLogger;
}

void QtLogger::InitLogger(int nType)  //可以 多次动作
{
	qInstallMessageHandler(QtLogger::loghanderCallback);
	m_nLogType = nType;
}

void LoggerWriter::on_toLogger(int nType,const QString& strlog)
{
	QDir d;
	static QString strApp = qApp->applicationName();
	static QString strLogPath = qApp->applicationDirPath() + "/Logs";
	d.mkpath(strLogPath);

	QString strData = QDateTime::currentDateTime().toString("_yyyyMMdd");
	QString strLogFile = QString("%1/%2%3.txt").arg(strLogPath).arg(strApp,strData);

	if(nType < m_ptCaller->GetLogType())
	{
		return;
	}
	
	if(!m_File.isOpen())
	{
		m_File.setFileName(strLogFile);

		if(!m_File.open(QIODevice::WriteOnly | QIODevice::Append))
		{
			return;
		}
	}

	if(m_cDate.date() != QDateTime::currentDateTime().date())
	{
		m_cDate.date() = QDateTime::currentDateTime().date();
		m_File.close();
		QDate data = QDateTime::currentDateTime().date().addDays(-30);
		QFile::remove(strLogPath + strApp + data.toString("_yyyMMdd"));
		m_File.setFileName(strLogFile);

		if(!m_File.open(QIODevice::WriteOnly | QIODevice::Append))
		{
			return;
		}
	}

	QTextStream text_stream(&m_File);
	text_stream << strlog << "\r\n";
	m_File.flush();
}


void QtLogger::loghanderCallback(QtMsgType type, const QMessageLogContext &context,const QString & msg)
{
	QString strType;

	switch(type)
	{
	case QtInfoMsg:
		strType = QString("Info:");
		break;

	case QtDebugMsg:
		strType = QString("Debug:");
		break;

	case QtWarningMsg:
		strType = QString("Warning:");
		break;

	case QtCriticalMsg:
		strType = QString("Critical:");
		break;

	case QtFatalMsg:
		strType = QString("Fatal:");
	}

	QString context_info = QString("(%1,%2)").arg(QString(context.file)).arg(context.line);
	QString current_datestr = QDateTime::currentDateTime().toString("yyyy-MM-dd hh:mm:ss.zzz ");
	QString message = QString("%1 %2 %3").arg(current_datestr,strType,msg);
	//message.append(context_info);
	emit QtLogger::getLogger()->evt_rawLog((int)type, msg);
	emit QtLogger::getLogger()->evt_toLogger((int)type,message);
}