import sys
import os
import ffmpeg
from tqdm import tqdm

# Parameters
segment_duration = 60 # Default 1 minute

def main():
    # Get first argument. If there is no first argument, throw error
    if len(sys.argv) < 2:
        print('Error: please specify video file')
        exit(1)
    elif len(sys.argv) > 2:
        print('Warning: too many arguments')
        
    input_file_path = sys.argv[1]
    file_extension = os.path.splitext(input_file_path)[1]
    
    # Create a folder to save the videos
    output_folder = input_file_path + '_output'
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    
    # Get video duration in seconds
    duration = int(float(ffmpeg.probe(input_file_path)["format"]["duration"]))
    
    # Create all clips
    for i in tqdm(range(0, duration, segment_duration)):
        start_time_seconds = i
     
        output_file_path = os.path.join(output_folder, str(start_time_seconds) + file_extension)
        
        # Cut with ffmpeg
        (
        ffmpeg.input(input_file_path, ss=start_time_seconds, loglevel='quiet')
        .output(output_file_path, c='copy', t=segment_duration)
        .run()
        )
    
if __name__ == '__main__':
    main()
