#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const char* getfield(char* line, int num)
{
    const char* tok;
    for (tok = strtok(line, ",");
            tok && *tok;
            tok = strtok(NULL, ",\n"))
    {
        if (!--num)
            return tok;
    }
    return NULL;
}

int main()
{
    FILE* stream = fopen("data1_mfcc.csv", "r");
    FILE* fp = fopen("data1_mfcc_out.csv", "w");
	int idx = 0, l, n, size =0;
	//int ar[]= { 100,3180, 6500, 8180, 12200, 13920, 15900,16340,19660,22140,28000,28560,30060,30940,34780,36520,39040,42740,47800,49700,54820,58400,60460,65920,76760,78200,79280,80680,82020,82940};
    int ar[50];
    FILE* fr = fopen("time.txt", "r");
	while( fscanf(fr, "%d,", &n) > 0 ) // parse %d followed by ','
    {
    	ar[size++] = n;
    }
	char line[1024];
    while (fgets(line, 1024, stream))
    {
        char* tmp = strdup(line);
        //printf("Field 3 would be %s\n", line );
        //free(tmp);
        //tmp = strdup(line);
        //printf("Field 3 would be %s \n", getfield(tmp, 4) );
        // NOTE strtok clobbers tmp
        l++;
        int n = strlen(line);
        line[n-1] = '\0';
        if(abs(l - ar[idx]) <= 3)
        {
        	//fprintf(fp,"%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,1\n",getfield(tmp, 1),getfield(tmp, 2),getfield(tmp, 3),getfield(tmp, 4),getfield(tmp, 5),getfield(tmp, 6),getfield(tmp, 7),getfield(tmp, 8),getfield(tmp, 9),getfield(tmp, 10),getfield(tmp, 11),getfield(tmp, 12),getfield(tmp, 13) );
				fprintf(fp,"%s,1\n", line);
		}
		else if(abs(ar[idx] - l) <=9 && abs(ar[idx] - l) >= 5)
		//fprintf(fp,"%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,0\n",getfield(tmp, 1),getfield(tmp, 2),getfield(tmp, 3),getfield(tmp, 4),getfield(tmp, 5),getfield(tmp, 6),getfield(tmp, 7),getfield(tmp, 8),getfield(tmp, 9),getfield(tmp, 10),getfield(tmp, 11),getfield(tmp, 12),getfield(tmp, 13) );
			fprintf(fp,"%s,0\n", line);
		if(l - ar[idx] > 9)
			if(idx<size)
				idx++;
        free(tmp);
    }
    printf("\n%d\n", l);
    fclose(fp);
    fclose(stream);
    fclose(fr);
}
