// std::fstream file("plot.txt", std::ios_base::in);
//   float x, y, theta, x_obs, y_obs, z_obs;
//   while (file >> x >> y)
//   { 
//     glColor3f(0,1,0); 
//     glPushMatrix(); 
//     glTranslatef(x * 10, 0, y * 10);
//     // glRotatef(theta, 0, 1, 0);   
//     glutSolidCube(1); 
    



//     while(file >> x_obs>> y_obs >> z_obs){
//       if(x_obs == -1 and y_obs == -1 and z_obs == -1)
//         break;
      
//       glColor3f(1,.5, .5); 
//       glBegin(GL_POINT);
//       glVertex3f(x_obs,y_obs,z_obs);
//       glEnd();
    
//     }
//     glPopMatrix();

//   }