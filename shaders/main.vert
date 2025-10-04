#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCoord;
layout (location = 2) in float aBlockIndex;
layout (location = 3) in float aNormalIndex;

out vec2 TexCoord;
flat out uint TexIndex;
out vec3 Normal;
flat out uint NormalIndex;
out vec3 FragPos;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

vec3 normals[6] = vec3[6](
	vec3(0.0f, 0.0f, -1.0f), // Back
	vec3(0.0f, 0.0f, 1.0f),  // Front
	vec3(1.0f, 0.0f, 0.0f),  // Left
	vec3(-1.0f, 0.0f, 0.0f), // Right
	vec3(0.0f, -1.0f, 0.0f), // Bottom
	vec3(0.0f, 1.0f, 0.0f)   // Top
);

void main() {

	gl_Position = projection * view * model * vec4(aPos, 1.0f);
	FragPos = vec3(model * vec4(aPos, 1.0f));

	TexCoord = aTexCoord;
	TexIndex = uint(aBlockIndex);
	Normal = normals[uint(aNormalIndex)];
	NormalIndex = uint(aNormalIndex);
}