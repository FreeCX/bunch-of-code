#include <iostream>
#include <fstream>
#include "shader.hpp"

ShaderProgram::ShaderProgram() {
}

ShaderProgram::~ShaderProgram() {
    glDeleteProgram(program);
}

void ShaderProgram::create() {
    program = glCreateProgram();
}

char* readFile(const char* fileName) {
    std::ifstream is(fileName, std::ios::in|std::ios::binary|std::ios::ate);
    if (!is.is_open()) {
        std::cerr << "Unable to open file " << fileName << std::endl;
        exit(1);
    }

    long size = is.tellg();

    auto buffer = new char[size+1];
    is.seekg(0, std::ios::beg);
    is.read (buffer, size);
    is.close();
    buffer[size] = 0;
    return buffer;
}

GLuint ShaderProgram::compileShader(const char* fileName, GLenum shaderType) {
    GLuint handler;

    // get a shader handler
    handler = glCreateShader(shaderType);
    // read the shader source from a file
    // conversions to fit the next function
    const char* buffer = readFile(fileName);
    // pass the source text to GL
    glShaderSource(handler, 1, &buffer, 0);
    // finally compile the shader
    glCompileShader(handler);
    return handler;
}

void ShaderProgram::addShader(const char* fileName, GLenum shaderType) {
    auto shader = compileShader(fileName, shaderType);
    glAttachShader(program, shader);
};

void ShaderProgram::link() {
    glLinkProgram(program);
}

void ShaderProgram::run() {
    glUseProgram(program);
}

void ShaderProgram::stop() {
    glUseProgram(0);
}

void ShaderProgram::uniform(const char* varName, int value) {
    glUniform1i(glGetUniformLocation(program, varName), value);
}

void ShaderProgram::uniform(const char* varName, float value) {
    glUniform1f(glGetUniformLocation(program, varName), value);
}

void ShaderProgram::uniform(const char* varName, glm::vec2 value) {
    glUniform2f(glGetUniformLocation(program, varName), value.x, value.y);
}

void ShaderProgram::uniform(const char* varName, glm::vec3 value) {
    glUniform3f(glGetUniformLocation(program, varName), value.x, value.y, value.z);
}

void ShaderProgram::uniform(const char* varName, glm::vec4 value) {
    glUniform4f(glGetUniformLocation(program, varName), value.x, value.y, value.z, value.w);
}

void ShaderProgram::uniform(const char* varName, glm::mat4 projection) {
    glUniformMatrix4fv(glGetUniformLocation(program, varName), 1, GL_FALSE, glm::value_ptr(projection));
}