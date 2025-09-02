cmake_minimum_required(VERSION 3.15)
set(CMAKE_CXX_STANDARD 23)

file(GLOB PROTO_FILES "${CMAKE_CURRENT_SOURCE_DIR}/*.proto")

foreach(proto ${PROTO_FILES})
    get_filename_component(proto_name ${proto} NAME_WE)

    set(proto_src "${CMAKE_CURRENT_BINARY_DIR}/${proto_name}.pb.cc")
    set(proto_hdr "${CMAKE_CURRENT_BINARY_DIR}/${proto_name}.pb.h")
    set(grpc_src "${CMAKE_CURRENT_BINARY_DIR}/${proto_name}.grpc.pb.cc")
    set(grpc_hdr "${CMAKE_CURRENT_BINARY_DIR}/${proto_name}.grpc.pb.h")

    add_custom_command(
        OUTPUT ${proto_src} ${proto_hdr} ${grpc_src} ${grpc_hdr}
        COMMAND protobuf::protoc
        ARGS --grpc_out ${CMAKE_CURRENT_BINARY_DIR}
             --cpp_out ${CMAKE_CURRENT_BINARY_DIR}
             -I ${CMAKE_CURRENT_SOURCE_DIR}
             --plugin=protoc-gen-grpc=$<TARGET_FILE:gRPC::grpc_cpp_plugin>
             ${proto}
        DEPENDS ${proto}
    )

    list(APPEND PROTO_SRCS ${proto_src})
    list(APPEND PROTO_HDRS ${proto_hdr})
    list(APPEND GRPC_SRCS ${grpc_src})
    list(APPEND GRPC_HDRS ${grpc_hdr})
endforeach()

add_library(apis STATIC ${PROTO_SRCS} ${PROTO_HDRS} ${GRPC_SRCS} ${GRPC_HDRS})
target_include_directories(apis PUBLIC "${CMAKE_CURRENT_BINARY_DIR}")
target_link_libraries(apis PUBLIC protobuf::protobuf gRPC::grpc++)