#version 410 core

layout (location = 0) out vec4 FragColor;
uniform sampler2DArray textureArray;

in vec2 TexCoord;
flat in uint TexIndex;
in vec3 Normal;
flat in uint NormalIndex;
in vec3 FragPos;

void main() {
    vec3 lightValue;

    switch (NormalIndex) {
        case 0u:
          lightValue = vec3(0.86f); // Back
          break;
        case 1u:
          lightValue = vec3(0.86f); // Front
          break;
        case 2u:
          lightValue = vec3(0.8f); // Left
          break;
        case 3u:
          lightValue = vec3(0.8f); // Right
          break;
        case 4u:
          lightValue = vec3(0.65f); // Bottom
          break;
        case 5u:
          lightValue = vec3(1.0f); // Top
          break;
    }

    vec4 final = texture(textureArray, vec3(TexCoord, TexIndex));

    FragColor = vec4(final.rgb * lightValue, final.a);
}