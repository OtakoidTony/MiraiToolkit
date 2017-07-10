import sys
import os

header_length = 72 # not sure if this is correct. definitely >= 72
chunk_size = 1000

def draw_progress_bar(percent, barLen = 20):
    """
    Shows progress of directory processing. 
    """
    sys.stdout.write("\r")
    progress = ""
    for i in range(barLen):
        if i < int(barLen * percent):
            progress += "="
        else:
            progress += " "
    sys.stdout.write("[ %s ] %.2f%%" % (progress, percent * 100))
    sys.stdout.flush()

def is_header(byte_string):
    """
    Check if bytestring is header. 
    """
    return byte_string[:4] == b"CTPK" and len(byte_string) == header_length

def get_headers(file_name):
    """
    Get all the CTPK headers in the file. 

    Note: Not really sure how CTPK headers work. They always begin with 
    b"CTPK" but unsure what they end with. Possibly b"ctpk" which makes sense 
    but there always seems to be more consistent data after that. 
    """
    headers = []
    with open(file_name, "rb") as input_file:
        peek_chunk = True
        while peek_chunk:
            peek_chunk = input_file.peek(chunk_size)[:chunk_size]
            if b"CTPK" in peek_chunk:
                input_file.read(1)
            else:
                input_file.read(len(peek_chunk))
            if is_header(peek_chunk[:header_length]):
                headers.append(peek_chunk[:header_length])
    if len(headers) == 0:
        raise SystemExit("\nNo valid header found. ")
    return headers

def write_header(file, header):
    """
    Write the header to a file. 
    """
    file.write(header)

def advance_to_image(file, header):
    """
    Advance the file the end of the header. 
    """
    peek_chunk = file.peek(chunk_size)[:chunk_size]
    while peek_chunk and peek_chunk[:len(header)] != header:
        if header in peek_chunk:
            file.read(1)
        else:
            file.read(len(peek_chunk))
        peek_chunk = file.peek(chunk_size)[:chunk_size]
    file.read(len(header))

def copy_image(file, file_name, directory, header, headers, index):
    """
    Copy the data from the current header until the next header. 
    """
    next_header = (headers + [b""])[index + 1]
    peek_chunk = file.peek(chunk_size)[:chunk_size]
    with open(directory + "/" + file_name + "_image_" + str(index), "wb") as output_file:
        write_header(output_file, header)
        while peek_chunk and peek_chunk[:len(next_header)] != next_header:
            chunk = b""
            if next_header in peek_chunk:
                chunk = file.read(1)
            else:
                chunk = file.read(chunk_size)
            output_file.write(chunk)
            peek_chunk = file.peek(chunk_size)[:chunk_size]
    return peek_chunk == b""

def process_file(file_name):
    """
    Split the given file into parts based on CTPK headers and place the split 
    files in a subdirectory. 
    """
    directory = file_name + "_images"
    trimmed_file_name = file_name
    if "/" in file_name:
        root = file_name[:file_name.rfind("/") + 1]
        trimmed_file_name = file_name[file_name.rfind("/") + 1:]
        directory = root + trimmed_file_name + "_images"
    if not os.path.exists(directory):
        os.makedirs(directory)
    headers = get_headers(file_name)
    with open(file_name, "rb") as input_file:
        for i, header in enumerate(headers):
            advance_to_image(input_file, header)
            copy_image(input_file, trimmed_file_name, directory, header, headers, i)

def is_CTPK_file(name):
    """
    Check if the bytestring b"CTPK" can be found in the file. 
    """
    if os.path.isdir(name):
        return False
    with open(name, "rb") as input_file:
        chunk = True
        while chunk:
            chunk = input_file.read(1000)
            if b"CTPK" in chunk:
                return True
    return False

def main():
    """
    Check if argument is either a file or directory. If it is a file, process 
    it. If it is a directory, process all CTPK files in the directory. 
    """
    if len(sys.argv) != 2:
        raise SystemExit("Only argument must be valid file or directory name. ")
    arg = sys.argv[1]
    if os.path.isfile(arg):
        if not is_CTPK_file(arg):
            raise SystemExit("Invalid CTPK file. ")
        print("Processing...")
        process_file(arg)
        print("Done!")
    elif os.path.isdir(arg):
        root = ""
        if os.path.isdir(arg):
            root = arg
        elif os.path.isdir(arg[:arg.rfind("/")]):
            root = arg[:arg.rfind("/")]
        elif os.path.isdir(arg[:-1][:arg[:-1].rfind("/")]):
            root = arg[:-1][:arg[:-1].rfind("/")]
        file_names = [root + "/" +  name for name in os.listdir(arg) if is_CTPK_file(root + "/" + name)]
        if len(file_names) == 0:
            raise SystemExit("No CTPK files found in directory. ")
        print("Files processing:")
        for file_name in file_names:
            print(file_name)
        for i, file_name in enumerate(file_names):
            draw_progress_bar(i/len(file_names))
            process_file(file_name)
        draw_progress_bar(1.0)
        print("")
    else:
        raise SystemExit("Argument must be valid file or directory name. ")

main()
