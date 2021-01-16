cmake_minimum_required(VERSION 3.0)

project(particles)

find_package(OpenGL REQUIRED COMPONENTS OpenGL EGL GLX)
find_package(GLEW REQUIRED)
find_package(PkgConfig REQUIRED)
find_package(Freetype REQUIRED)
pkg_check_modules(GLFW REQUIRED glfw3)

include_directories(
    ${OPENGL_INCLUDE_DIR}
    ${GLFW_INCLUDE_DIRS}
    ${GLEW_INCLUDE_DIRS}
    ${FREETYPE_INCLUDE_DIRS}
)
add_executable(particles 
    src/window.cpp 
    src/error.cpp 
    src/main.cpp
    src/shader.cpp 
    src/vertex.cpp
    src/font.cpp
    src/points.cpp
)

execute_process(COMMAND ${CMAKE_COMMAND} -E create_symlink ${CMAKE_CURRENT_SOURCE_DIR}/assets
                                                           ${CMAKE_CURRENT_BINARY_DIR}/assets)

target_compile_features(particles PRIVATE cxx_aggregate_default_initializers)
target_link_libraries(particles PRIVATE
    PRIVATE OpenGL::OpenGL OpenGL::EGL OpenGL::GLX
    ${GLFW_LIBRARIES}
    ${GLEW_LIBRARIES}
    ${FREETYPE_LIBRARIES}
)