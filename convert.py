import pysrt
import csv
import os


def timestamp_to_seconds(timestamp: object) -> object:
    total_seconds = timestamp.seconds + 60 * (timestamp.minutes + 60 * timestamp.hours)
    return total_seconds + timestamp.milliseconds / 1000


def csv_to_dict(fpath):
    dict_from_csv = {}
    with open(fpath, mode='r', encoding='utf-8') as inp:
        reader = csv.reader(inp)
        dict_from_csv = {rows[0]: rows[1] for rows in reader}
    return dict_from_csv


def convert_srt_to_tsv(name, srt_path, tsv_path, speakers):
    srt = pysrt.open(os.path.join(srt_path, name))
    fname = name.split(".", 1)[0] + ".tsv"
    f = open(os.path.join(tsv_path, fname), "w", encoding="utf-8", newline="")
    tsv_writer = csv.writer(f, delimiter="\t")
    speaker = "Unknown"
    transcription = ""
    lastcolor = color = "black"
    for item in srt:
        start_time = timestamp_to_seconds(item.start)
        end_time = timestamp_to_seconds(item.end)
        text_parsed = item.text.split(":", 1)
        speaker = "Unknown Speaker"
        transcription = ""
        if len(text_parsed) == 2:
            speaker = text_parsed[0].strip()
            color = speakers.get(speaker, "speaker-not-found")
            if color == "speaker-not-found":
                transcription = item.text.strip()
                print('"%s" is not in speakerlist.csv (included in transcription block)' % speaker)
            else:
                transcription = text_parsed[1].strip()
                speaker = "<font color='%s'><b>%s</b></font>" % (color, speaker)
                lastcolor = color
                tsv_writer.writerow([start_time, end_time, speaker, "Speaker"])
            color = lastcolor
        else:
            transcription = item.text.strip()
        transcription = transcription.replace("\n", " ")
        transcription = "<font color='%s'>%s</font>" % (color, transcription)
        tsv_writer.writerow([start_time, end_time, transcription, "Transcription"])
    f.close()


def main():
    srt_path = os.path.join(os.getcwd(), "input-srt")
    tsv_path = os.path.join(os.getcwd(), "output-tsv")
    speaker_dict = csv_to_dict(os.path.join(os.getcwd(), "speakerlist.csv"))
    print(speaker_dict)
    files = os.listdir(srt_path)
    count = 0
    for file in files:
        count += 1
        print(file + ", ", count)
        convert_srt_to_tsv(file, srt_path, tsv_path, speaker_dict)


if __name__ == '__main__':
    main()
