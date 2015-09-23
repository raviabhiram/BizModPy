#include<iostream>
#include<unistd.h>
#include<stdlib.h>
using namespace std;
int main()
{
	int i=1;
	sleep(86400);
	system("sudo init 0");
	return 0;
}
