#include <stdio.h>
#include <math.h>

float circle_size = 50.0f;

float Xfunc(float t)
{
	return cos(t) * (t / circle_size);
}

float Yfunc(float t)
{
	return sin(t) * (t / circle_size);

}

float Zfunc(float t)
{
	// return cos(t) * sin(t) * t ;
	return 0.0f;
}

float Wfunc(float t)
{
	return 0.0f;
} 
	

int main(int argc, char **argv)
{
	float t;

	for( t = 0 ;  ; t += 0.005f)
	{
		// X Y Z R G B
		printf("%f %f %f %f %f %f ", Xfunc(t), Yfunc(t), Zfunc(t), fabs(sin(t)), fabs(cos(t)), fabs(sin(t)*cos(t)) );
	}
	return 0;
}
