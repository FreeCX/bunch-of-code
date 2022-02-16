CXX=g++
CFLAGS=-std=c++14 -Wall $(shell pkg-config --cflags freetype2)
LFLAGS=$(shell pkg-config --libs freetype2)
app=fb_gui_demo
objects := $(patsubst %.cpp,%.o,$(wildcard src/*.cpp))

all: $(objects)
	$(CXX) $(objects) $(LFLAGS) -o $(app)
$(objects): %.o: %.cpp
	$(CXX) $(CFLAGS) -c $< -o $@
clean:
	-$(RM) $(app) $(objects)
