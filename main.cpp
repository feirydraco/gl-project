#include <stdio.h>
#include <stdlib.h>
#include<iostream>
#include<fstream>
#include <GL/glut.h> 
#include <GL/gl.h>

int press_x, press_y; 
int x_shift,z_shift; //glutLookAT
int release_x, release_y; 
float x_angle = 0.0; 
float y_angle = 0.0; 
float scale_size = 1; 

int xform_mode = 0; 


void (*varFunc)();
int menu_mode = 0;


#define XFORM_NONE    0 
#define XFORM_ROTATE  1
#define XFORM_SCALE 2 

int stage = 0; 
int case_id = 0; 
float base_translate = 0; 
float low_rotate = 0; 
float up_rotate = 90; 
float hammer_rotate = 0; 

int show_axis=-1; 
int poly_fill = 0;

GLfloat objectXform[4][4] = {
	1,0,0,0,
	0,1,0,0,
	0,0,1,0,
	0,0,0,1}; 

///////////////////////////////////////////

void draw_axes()
{
  glLineWidth(3);        
  glBegin(GL_LINES); 
    glColor3f(1,0,0);    // red: x; green: y; blue: z
    glVertex3f(0,0,0); 
    glVertex3f(4,0,0); 
    glColor3f(0,1,0);  
    glVertex3f(0,0,0); 
    glVertex3f(0,4,0); 
    glColor3f(0,0,1); 
    glVertex3f(0,0,0); 
    glVertex3f(0,0,4); 
  glEnd(); 
  glLineWidth(1.0); 
}

////////////////////////////////////////////// 

void draw_scene(int cid)
{		
	
		glColor3f(1,1,0); 
		glutWireCube(3); 
    glTranslatef(1,0,2); 
     glutWireCube(1); 
		

	// 	if (show_axis==1) draw_axes(); 
	//   //gluCylinder(p, 1.5, 1.5,1.5, 30, 30); //base 
  //   //glPushMatrix();


  //   //glPopMatrix(); 
	// 	//glRotatef(low_rotate, 0, 0, 1); // rotate lower arm
	// 	if (show_axis==2) draw_axes(); 
	// 	//gluCylinder(p, 0.5, 0.5, 2, 10, 10);  // lower arm
	// //	glTranslatef(0,0,2.0); 
	// 	//glRotatef(up_rotate, 0, 1, 0);   // rotate upper arm  
	// 	if (show_axis==3) draw_axes(); 
	// 	//gluCylinder(p, 0.5, 0.5, 2.5, 10, 10); // upper arm 
  //       glTranslatef(0,0,2.5); 
	// 	glRotatef(90, 1, 0, 0); 
	// 	glRotatef(hammer_rotate, 0, 1, 0); 
	// 	glTranslatef(0,0,-1); 
	// 	if (show_axis==4) draw_axes(); 
	// 	//gluCylinder(p,0.5, 0.5, 2, 10, 10); 


}
//////////////////////////////////////////////////

// void ReadAndDrawPoint()
// {


//     float posx,posy,theta;
// 	  if(std::cin>>posx>>posy>>theta) {
//       // theta = (theta*180)/3.14;
//       std::cout<<posx<<posy<<theta;
//       //printf("POS READ : %f %f %f", posx, posx, theta);
//       //ready = 1;
//       glMatrixMode(GL_MODELVIEW); 
//         glLoadMatrixf((GLfloat*) objectXform); 
//         glTranslatef(posx/10,posy/10,0); 
//         glGetFloatv( GL_MODELVIEW_MATRIX, (GLfloat *) objectXform );
//         show_axis =1;  

//         glMatrixMode(GL_MODELVIEW); 
//         glLoadMatrixf((GLfloat*) objectXform); 
//         glRotatef(theta, 0, 0, 1); 
//         glGetFloatv( GL_MODELVIEW_MATRIX, (GLfloat *) objectXform );	
//       }
//       glutPostRedisplay(); 

      
		
// }


//////////////////////////////////////////////////////

void display()
{
  glEnable(GL_DEPTH_TEST);  
  glClearColor(0,0,0,1); 

  glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT);
  

  //If enabled, use the current lighting parameters to compute the vertex color. Otherwise, simply associate the current color with each vertex
  glEnable(GL_LIGHTING); 
  glEnable(GL_LIGHT0); 

  glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE); 

  glEnable(GL_NORMALIZE); //?
  
  //If enabled, have ambient and diffuse material parameters track the current color.
  glEnable(GL_COLOR_MATERIAL);  

  glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE); 

  GLfloat light_ambient[] = {.0,.0,.0,1}; 
  GLfloat light_diffuse[] = {.8,.8,.8,1};
  GLfloat light_specular[] = {1,1,1,1}; 
  GLfloat light_pos[] = {0,0,0,1}; 

  glMatrixMode(GL_PROJECTION); 
  glLoadIdentity(); 
  gluPerspective(10, 1, .1, 150); 
  
  glMatrixMode(GL_MODELVIEW); 
  glLoadIdentity(); 

  glLightfv(GL_LIGHT0,GL_AMBIENT, light_ambient); 
  glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse); 
  glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular); 
  glLightfv(GL_LIGHT0, GL_POSITION, light_pos);
 
  GLfloat mat_specular[] = {.7, .7, .7,1}; 
  GLfloat mat_shine[] = {60}; 

  glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_specular); 
  glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_shine); 
  
  gluLookAt(30,30,30,x_shift,0,z_shift,0,1,0);

  glRotatef(x_angle, 0, 1,0); 
  glRotatef(y_angle, 1,0,0); 
  glScalef(scale_size, scale_size, scale_size); 
  
  glDisable(GL_LIGHTING); 
  draw_axes(); 
  glEnable(GL_LIGHTING); 

	if (!poly_fill)glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
	else glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);
	if (!poly_fill) glDisable(GL_LIGHTING); 
	else glEnable(GL_LIGHTING); 

  
  glPushMatrix(); 
  glTranslatef(0,-5,0); 
  glScalef(200, 1, 200);       // floor
  glutSolidCube(1); 
  glPopMatrix(); 
  glLineWidth(1);
  
  

  std::fstream file("plot.txt", std::ios_base::in);
  float x, y, theta, x_obs, y_obs, z_obs;
  while (file >> x >> y)
  { 
    glColor3f(0,1,0); 
    glPushMatrix(); 
    glTranslatef(x * 10, 0, y * 10);
    // glRotatef(theta, 0, 1, 0);   
    glutSolidCube(1); 
    



    while(file >> x_obs>> y_obs >> z_obs){
      if(x_obs == -1 and y_obs == -1 and z_obs == -1)
        break;
      
      glColor3f(1,.5, .5); 
      glBegin(GL_POINT);
      glVertex3f(x_obs,y_obs,z_obs);
      glEnd();
    
    }
    glPopMatrix();

  }

  glRotatef(-90, 1, 0, 0); 

  glMultMatrixf((const float*)objectXform); 

  draw_scene(case_id); 

  glutSwapBuffers(); 
}

///////////////////////////////////////////////////////////

void mymouse(int button, int state, int x, int y)
{
  if (state == GLUT_DOWN) {
    press_x = x; press_y = y; 
    if (button == GLUT_LEFT_BUTTON)
      xform_mode = XFORM_ROTATE; 
	 else if (button == GLUT_RIGHT_BUTTON) 
      xform_mode = XFORM_SCALE; 
  }
  else if (state == GLUT_UP) {
	  xform_mode = XFORM_NONE; 
  }
}

/////////////////////////////////////////////////////////

void mymotion(int x, int y)
{
    if (xform_mode==XFORM_ROTATE) {
      x_angle += (x - press_x);//5.0; 
      if (x_angle > 180) x_angle -= 360; 
      else if (x_angle <-180) x_angle += 360; 
      press_x = x; 
	   
      // y_angle += (y - press_y);//5.0; 
      // if (y_angle > 180) y_angle -= 360; 
      // else if (y_angle <-180) y_angle += 360; 
      // press_y = y; 
    }
	else if (xform_mode == XFORM_SCALE){
      float old_size = scale_size;
      scale_size *= (1+ (y - press_y)/60.0); 
      if (scale_size <0) scale_size = old_size; 
      press_y = y; 
    }
	glutPostRedisplay(); 
}

///////////////////////////////////////////////////////////////

void mykey(unsigned char key, int x, int y)
{



        switch(key) {



		case 'q': exit(1);
			break;
		case 'r':  x_shift=0, z_shift = 0; 
			break; 
		case 'u': up_rotate +=5; show_axis=3;
			break; 
		case 'h': hammer_rotate +=5;show_axis=4; 
			break; 
		case 'f': poly_fill = !poly_fill; 
			break; 
		case 'n': show_axis=-1;
			break;
		case 'w':
			glMatrixMode(GL_MODELVIEW); 
			glLoadMatrixf((GLfloat*) objectXform); 
			glTranslatef(.1,0,0); 
			glGetFloatv( GL_MODELVIEW_MATRIX, (GLfloat *) objectXform );
			show_axis =1; 
			break; 
		case 's': 
      
      //gluLookAt(30,30,30,x_shift,0,z_shift,0,1,0);
			glMatrixMode(GL_MODELVIEW); 
			glLoadMatrixf((GLfloat*) objectXform); 
			glTranslatef(-1,0,0); 
			glGetFloatv( GL_MODELVIEW_MATRIX, (GLfloat *) objectXform );
			//show_axis=1; 
			break; 
		case 'a':
			glMatrixMode(GL_MODELVIEW); 
			glLoadMatrixf((GLfloat*) objectXform); 
			glRotatef(30, 0, 0, 1); 
			glGetFloatv( GL_MODELVIEW_MATRIX, (GLfloat *) objectXform );	
			break; 
		case 'd': 
			glMatrixMode(GL_MODELVIEW); 
			glLoadMatrixf((GLfloat*) objectXform); 
			glRotatef(-30, 0, 0, 1); 
			glGetFloatv( GL_MODELVIEW_MATRIX, (GLfloat *) objectXform );	
			break; 
		}
glutPostRedisplay(); 
}



///////////////////////////////////////////////////////////


void SpecialInput(int key, int x, int y)
{
  switch(key)
  {
  case GLUT_KEY_UP:
  z_shift -= 3;
  break;	
  case GLUT_KEY_DOWN:
  z_shift += 3;
  break;
  case GLUT_KEY_LEFT:
  x_shift -= 3;
  break;
  case GLUT_KEY_RIGHT:
  x_shift += 3;
  break;
}
glutPostRedisplay();
}
///////////////////////////////////////////////////////////////





void menuFunc(int op)
{
	if(op==1)
		menu_mode = 0;
	else if(op==2)
		menu_mode = 1;
	else if(op==3)
		menu_mode = 2;
  else if(op==4)  //TODO
		menu_mode = 3;  
	else if(op==5)
		exit(0);
	glutPostRedisplay();
}


///////////////////////////////////////////////////////////

int main(int argc, char** argv) 
{
  glutInit(&argc, argv); 
  glutInitDisplayMode(GLUT_RGB|GLUT_DOUBLE|GLUT_DEPTH); 
  glutInitWindowSize(1000,1000); 
  
  glutCreateWindow("proj"); 

  glutCreateMenu(menuFunc);
	glutAddMenuEntry("Trajectory",1);
	glutAddMenuEntry("Plot Interest Points",2);
	glutAddMenuEntry("Draw Interest Lines",3);
  glutAddMenuEntry("Model Objects",4);
	glutAddMenuEntry("Quit",5);
	glutAttachMenu(GLUT_MIDDLE_BUTTON);


  glutDisplayFunc(display); 
  glutMouseFunc(mymouse); 
  glutMotionFunc(mymotion);
  glutSpecialFunc(SpecialInput);
  glutKeyboardFunc(mykey);
  // glutIdleFunc(display) ;
  glutMainLoop(); 
}