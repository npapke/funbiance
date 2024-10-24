#version 100
#ifdef GL_ES
precision mediump float;
#endif
varying vec2 v_texcoord;
uniform sampler2D tex;
uniform float time;
uniform float width;
uniform float height;

void main () {
	gl_FragColor = texture2D( tex, v_texcoord ) * vec4(0.5, 0.5, 0.5, 0.5);
}
