#include<iostream>
using namespace std;

int main()
{
	FILE* fp = fopen("time.txt", "w");
	int h,m,s;
	while(1) {
	//h = 0;
	cin>>h>>m>>s;
	if(h ==0 && m==0 && s ==0)
		break;
	long long int  ms;
	ms = h*60*60 + m*60 + s;
	ms *= 2;
	fprintf(fp,"%d,", ms);
	}
	fclose(fp);
	return 0;
}
