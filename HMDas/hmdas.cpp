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
	QMenu* menu = ui.menuBar->addMenu(tr("关于"));

	menu->addAction(tr("关于"), [](){
		QDialog d;
		d.setModal(false);
		Ui::About aUi;
		QImage image;
		bool bRet = image.load(":/image/logo.png");
		aUi.setupUi(&d);
		if (bRet)
		{
			aUi.label_logo->setPixmap(QPixmap::fromImage(image));//在label上显示图片
		}
		d.exec();
	});
		
	menu->addAction(tr("关于软件"), [](){
		qApp->aboutQt();
	});

	//menu->add

}
