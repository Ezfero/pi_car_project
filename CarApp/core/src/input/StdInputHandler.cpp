#include "StdInputHandler.h"

#include <iostream>
#include <termios.h>
#include <unistd.h>

namespace car_app::core {

void StdInputHandler::start() {
    running_ = true;
    while(running_) {
        const char nextCommand = nextChar();
        if (!kCommandsMap.contains(nextCommand)) {
            continue;
        }
        auto command = kCommandsMap.at(nextCommand);
        commandQueue_.push(command);
    }
}

void StdInputHandler::stop() {
    running_ = false;
}

InputCommandQueue& StdInputHandler::getInputCommandQueue() {
    return commandQueue_;
}

char StdInputHandler::nextChar() const {
    char buf = 0;
    // TODO: here we are setting config on each read. Think about doing it only once when we start read and resetting at the end.
    termios old = {};
    tcgetattr(STDIN_FILENO, &old);
    termios newt = old;
    newt.c_lflag &= ~(ICANON | ECHO);  // disable buffering and echo
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);
    read(STDIN_FILENO, &buf, 1);
    tcsetattr(STDIN_FILENO, TCSANOW, &old);
    return buf;
}

} // namespace car_app::core