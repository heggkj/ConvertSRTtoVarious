import pysrt
import csv
import os
import re


def timestamp_to_seconds(timestamp: object) -> object:
    total_seconds = timestamp.seconds + 60 * (timestamp.minutes + 60 * timestamp.hours)
    return total_seconds + timestamp.milliseconds / 1000


def HHMMSS_to_seconds(timecode: str) -> int:
    ary = timecode.split(":")
    hours = int(ary[0])
    minutes = int(ary[1])
    seconds = int(ary[2])
    return (hours * 60 * 60) + (minutes * 60) + seconds


def csv_to_dict(fpath):
    dict_from_csv = {}
    with open(fpath, mode='r', encoding='utf-8') as inp:
        reader = csv.reader(inp)
        dict_from_csv = {rows[0]: rows[1] for rows in reader}
    return dict_from_csv


def get_env_row(s):
    a = s.split("|")
    start_time = HHMMSS_to_seconds(a[0].strip())
    end_time = HHMMSS_to_seconds(a[1].strip())
    annotation = a[2].strip()
    return [start_time, end_time, annotation]


def convert_srt_to_tsv(name, srt_path, tsv_path, speakers):
    srt = pysrt.open(os.path.join(srt_path, name))
    fname = name.split(".", 1)[0] + ".tsv"
    f = open(os.path.join(tsv_path, fname), "w", encoding="utf-8", newline="")
    tsv_writer = csv.writer(f, delimiter="\t")
    speaker = ""
    transcription = ""
    lastcolor = color = "black"
    env_ary = []
    for item in srt:
        start_time = round(timestamp_to_seconds(item.start), 3)
        end_time = round(timestamp_to_seconds(item.end), 3)
        env_ary = []
        running = True
        while running:
            try:
                found = re.search('\[\[(.+?)\]\]', item.text).group(1)
                item.text = item.text.replace("[[" + found + "]]", " ")
                env_ary.append(get_env_row(found))
            except AttributeError:
                running = False
                pass
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
        transcription = transcription.replace("\n", " ").strip()
        transcription = transcription.replace('"', '&quot;')
        if len(transcription) > 0:
            transcription = "<font color='%s'>%s</font>" % (color, transcription)
            if len(speaker) > 0:
                start_time = start_time + .001
            tsv_writer.writerow([start_time, end_time, transcription, "Transcription"])
        if len(env_ary) > 0:
            for env_item in env_ary:
                # anno = "<font color='%s'>[%s]</font>" % (color, env_item[2])
                anno = "[" + env_item[2] + "]"
                tsv_writer.writerow([env_item[0], env_item[1], anno, "Environment"])
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
        break


if __name__ == '__main__':
    main()
