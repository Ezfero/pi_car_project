cmake_minimum_required(VERSION 3.15)
set(CMAKE_CXX_STANDARD 23)

file(GLOB PROTO_FILES "${CMAKE_CURRENT_SOURCE_DIR}/*.proto")

# ==============================
# C++ Protobuf / gRPC generation
# ==============================

foreach(proto ${PROTO_FILES})
    get_filename_component(proto_name ${proto} NAME_WE)
    set(cpp_output_dir "${CMAKE_CURRENT_BINARY_DIR}/gen/cpp")

    set(proto_src "${cpp_output_dir}/${proto_name}.pb.cc")
    set(proto_hdr "${cpp_output_dir}/${proto_name}.pb.h")
    set(grpc_src "${cpp_output_dir}/${proto_name}.grpc.pb.cc")
    set(grpc_hdr "${cpp_output_dir}/${proto_name}.grpc.pb.h")

    add_custom_command(
        OUTPUT ${proto_src} ${proto_hdr} ${grpc_src} ${grpc_hdr}
        COMMAND protobuf::protoc
        ARGS --grpc_out ${cpp_output_dir}
             --cpp_out ${cpp_output_dir}
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
target_include_directories(apis PUBLIC "${cpp_output_dir}")
target_link_libraries(apis PUBLIC protobuf::protobuf gRPC::grpc++)


# ==============================
# Python Protobuf / gRPC generation
# ==============================

find_package(Python3 REQUIRED COMPONENTS Interpreter)

set(python_output_dir "${CMAKE_CURRENT_BINARY_DIR}/gen/py")

foreach(proto ${PROTO_FILES})
    get_filename_component(proto_name ${proto} NAME_WE)

    add_custom_command(
        OUTPUT
            "${python_output_dir}/${proto_name}_pb2.py"
            "${python_output_dir}/${proto_name}_pb2_grpc.py"
        COMMAND ${CMAKE_COMMAND} -E make_directory "${python_output_dir}"
        COMMAND ${Python3_EXECUTABLE} -m grpc_tools.protoc
            -I ${CMAKE_CURRENT_SOURCE_DIR}
            --python_out=${python_output_dir}
            --grpc_python_out=${python_output_dir}
            ${proto}
        DEPENDS ${proto}
        COMMENT "Generating Python gRPC files from ${proto_name}.proto"
        VERBATIM
    )

    list(APPEND PY_PROTO_SRCS
        "${python_output_dir}/${proto_name}_pb2.py"
        "${python_output_dir}/${proto_name}_pb2_grpc.py"
    )
endforeach()

add_custom_target(python_protos ALL
    DEPENDS ${PY_PROTO_SRCS}
)

add_dependencies(apis python_protos)