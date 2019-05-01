
#include <stdio.h>

int main(int argc, char **argv)
{
	float x=-5;
	for(;;)
	{
		printf("%f %f %f", x, 0.0, 0.0);
		if(x<5)
		{
			x+=0.01;
		}else{
			x=-5;
		}
	}
	return 0;
}
