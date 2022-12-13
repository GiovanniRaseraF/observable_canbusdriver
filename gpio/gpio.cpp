/*
Author: Giovanni Rasera
Description: GPIO comunication for BananaPi M2 Zero
*/

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <thread>

using namespace std::chrono_literals;

enum direction{IN, OUT};

class gpio{
    static std::string export_path; 
    static std::string unexport_path;
    static std::string basefolder;

    // gpio port number
    unsigned int port;
    
    public:
    // Direction

    // RAII connect
    gpio(unsigned int p) : port{p}{  
        std::ofstream exportfile{export_path};

        if(!exportfile){
            std::cerr << "cannot open export file" << std::endl;
            exit(1);
        }

        port = port % 32;
        exportfile << port << std::endl;

        std::cout << "opening port: " << port << std::endl;
    }

    gpio(const gpio &) = delete;
    gpio(gpio &&) = default;
    gpio &operator=(const gpio &) = delete;
    gpio &operator=(gpio &) = default;

    // check open
    std::fstream tryopenfile(const std::string &path){
        std::fstream ret{path};
        
        if(!ret){
            std::cerr << "cannot open file: " << path << std::endl;
            exit(1);
        }

        return ret;
    }

    // direction and edge
    int set_direction(const direction d){
        // export file in */gpioPORT/direction
        std::fstream directionfile = tryopenfile(basefolder + "/gpio" + std::to_string(port) + "/direction"); 

    }

    // writing and reading
    bool write(bool val){
        set_direction(IN);
        return val;   
    } 

    bool read(){
        return false;
    }

    // disconnect
    ~gpio(){
        std::ofstream unexportfile{unexport_path};

        if(!unexportfile){
            std::cerr << "cannot open unexport file" << std::endl;
            exit(1);
        }

        unexportfile << port << std::endl;

        std::cout << "closing port: " << port << std::endl;
    }
};

std::string gpio::export_path{"/sys/class/gpio/export"};
std::string gpio::unexport_path{"/sys/class/gpio/unexport"};
std::string gpio::basefolder{"/sys/class/gpio"};

#define GPIO_DEBUG
#ifdef GPIO_DEBUG
// Testing
int main(int argc, char** argv){
    if(argc < 2) return 1;

    std::stringstream ss{argv[1]};
    unsigned int port{0}; 
    try{
        ss >> port;
    }catch(std::ios_base::failure &err){
        std::cerr << err.what() << std::endl;
        exit(1);
    }

    gpio gpio29{port};

    std::string end = "no";
    while(end != "end"){
        std::cout << ":>";std::cin >> end;
    }
}
#endif