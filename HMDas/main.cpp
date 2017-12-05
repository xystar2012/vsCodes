#include "hmdas.h"
#include <QtWidgets/QApplication>

int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	HMDas w;
	w.show();
	return a.exec();
}
