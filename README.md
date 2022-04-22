# ConvertSRTtoVarious

### convert2SRT.py
This Python code converts SRT files to the TSV file format used by AudiAnnotate to create a manifest for the AudiAnnotate IIIF-compatible viewer. In this case, the annotations are blocks of transcriptions. The layers hold two values: Speaker and Transcription.

There are many ways to use AudiAnnotate to view A/V transcriptions. The converted sample in this repository looks like [this](https://kevinhegg.github.io/sample-conversion/simple-srt-to-tsv-conversion-example).

The code is easy to use:
1. Download convert.py.
2. Install the requirements (provided in this repo)
3. Create an input-srt folder and an output-srt folder in the same directory holding convert.py.
4. Create an "speakerslist.csv" file in the same directory and add Speaker Name/color pairs. Colors can be web-compatible nouns (e.g. red, green, blue) or hexidecimal strings (e.g. #FF0000, #00FF00, #0000FF).
5. Run convert.py. Results will be put in the output-srt folder.

Another way to convert SRT files to AudiAnnotate-ready TSV files is to put speakers in the Layer column and the transcripts in the Annotate column. In this way, the transcript can be sorted by speakers. This method generates fewer rows in the TSV file.

NOTE: This code has only be tested with SRT files generated through Otter.ai. It should work with other files but caveat emptor.

### convert2OHMS.py
This Python code converts specially formated SRT files to OHMS-ready (see [here](https://www.oralhistoryonline.org/) for details) transcripts. It has been tested with Otter.ai SRTs.

To prepare your SRT file, do the following:
1. After logging into Otter, open the conversation you want to convert
2. Select Export as SRT
3. Set the Export parameters as illustrated in the screen capture below
4. Place your SRT, which has been chunked into the greatest number of blocks[1], each holding one or two words, into the input-srt folder
5. Run the conversion utility. The resulting .TXT file will appear in the output-txt folder.

![Export-as-SRT-from-Otter ai](https://user-images.githubusercontent.com/1427371/164727949-5ea43d58-c75c-4782-9a54-2e7760c2caa2.png)

The sample provided looks like this when loaded into the OHMS viewer:

![Sample_ SRT to OHMS Converter screen capture](https://user-images.githubusercontent.com/1427371/164777618-823cca9d-e0e9-4e92-a1bc-af8a9391f81a.png)



[1] By chunking the SRT file into the smallest spans of time, my script is able to closely match SRT timestamps with OHMS intervals, which can be set to 30, 60, 120, 180, 240, or 300 seconds.
