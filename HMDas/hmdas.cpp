#include "hmdas.h"
#include <QMenuBar>
#include "ui_about.h"

#pragma execution_character_set("utf-8")

HMDas::HMDas(QWidget *parent)
	: QMainWindow(parent)
{
	ui.setupUi(this);

	InitUi();
}


HMDas::~HMDas()
{

}

void HMDas::InitUi()
{
	QMenu* menu = ui.menuBar->addMenu(tr("����"));

	menu->addAction(tr("����"), [](){
		QDialog d;
		d.setModal(false);
		Ui::About aUi;
		QImage image;
		bool bRet = image.load(":/image/logo.png");
		aUi.setupUi(&d);
		if (bRet)
		{
			aUi.label_logo->setPixmap(QPixmap::fromImage(image));//��label����ʾͼƬ
		}
		d.exec();
	});
		
	menu->addAction(tr("�������"), [](){
		qApp->aboutQt();
	});

	//menu->add

}
