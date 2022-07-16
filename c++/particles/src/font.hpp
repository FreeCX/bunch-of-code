#pragma once
#include <cstdint>
#include <iostream>
#include <map>

#include <GL/glew.h>

#include <GL/gl.h>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

#include <ft2build.h>
#include FT_FREETYPE_H

#include "error.hpp"
#include "shader.hpp"

/// Holds all state information relevant to a character as loaded using FreeType
struct Character {
    GLuint TextureID;   // ID handle of the glyph texture
    glm::ivec2 Size;    // Size of glyph
    glm::ivec2 Bearing; // Offset from baseline to left/top of glyph
    GLuint Advance;     // Horizontal offset to advance to next glyph
};

class Font {
  public:
    Font(const GLfloat width, const GLfloat height) : _width(width), _height(height) {}
    void shader(const char *vertex_shader, const char *fragment_shader);
    void load(const char *font_name, const uint16_t size);
    void render(std::string text, glm::vec3 pos, glm::vec3 color, GLfloat scale = 1.0f);

  private:
    GLfloat _width;
    GLfloat _height;
    std::map<GLchar, Character> Characters;
    ShaderProgram _shader;
    GLuint VAO, VBO;
};
