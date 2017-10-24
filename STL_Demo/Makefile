build : main.o hello.o
	g++ -o build  main.o -lpthread hello.o 
main.o : main.cpp
	g++ -std=c++11 -g -c main.cpp -Wl,--no-as-needed  -I /opt/boost_1.55/include -L /opt/boost_1.55/lib -lboost_filesystem -lboost_system 
hello.o : hello.h hello.cpp
	g++ -g -c hello.cpp
clean :
	rm main.o hello.o build