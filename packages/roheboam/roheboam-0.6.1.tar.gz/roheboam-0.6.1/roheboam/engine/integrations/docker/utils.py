def stream_docker_logs(log_generator):
    while True:
        try:
            output = log_generator.__next__()
            if "stream" in output:
                output_str = output["stream"].strip("\r\n").strip("\n")
                print(output_str)
        except StopIteration:
            print("Docker image build complete.")
            break
        except ValueError:
            print(f"Error parsing output from docker image build: {output}")
