# ConvertSRTtoAudiAnnotate

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
