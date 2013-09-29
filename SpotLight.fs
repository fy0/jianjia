varying vec3 N;  
varying vec3 v;  
  
void main (void)  
{  
    vec3 L = normalize(gl_LightSource[1].position.xyz - v);   
    vec3 E = normalize(-v);
    vec3 R = normalize(-reflect(L,N));   
  
    vec4 Iamb = gl_FrontLightProduct[1].ambient;  
    vec4 Idiff = gl_FrontLightProduct[1].diffuse * max(dot(N,L), 0.0);  
    vec4 Ispec = gl_FrontLightProduct[1].specular * pow(max(dot(R,E),0.0), 0.3 * gl_FrontMaterial.shininess);  

    gl_FragColor = gl_FrontLightModelProduct.sceneColor + Iamb + Idiff + Ispec;   
}  