#ifndef HMDAS_H
#define HMDAS_H

#include <QtWidgets/QMainWindow>
#include "ui_hmdas.h"

class HMDas : public QMainWindow
{
	Q_OBJECT

public:

	HMDas(QWidget *parent = 0);
	~HMDas();

protected:

	void InitUi();

private:
	Ui::HMDasClass ui;
};

#endif // HMDAS_H
