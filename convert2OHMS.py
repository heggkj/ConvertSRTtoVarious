import pysrt
import os


def timestamp_to_seconds(timestamp: object) -> object:
    total_seconds = timestamp.seconds + 60 * (timestamp.minutes + 60 * timestamp.hours)
    return total_seconds + timestamp.milliseconds / 1000


def format_timecode(interval):
    second = interval % 60
    minute = int((interval/60) % 60)
    hour = int(((interval/60)/60) % 60)
    return "[" + str(hour).zfill(2) + ":" + str(minute).zfill(2) + ":" + str(second).zfill(2) + "]"


def convert_srt_to_tsv(name, srt_path, txt_path, interval):
    srt = pysrt.open(os.path.join(srt_path, name))
    fname = name.split(".", 1)[0] + ".txt"
    f = open(os.path.join(txt_path, fname), "w", encoding="utf-8")
    transcription = ""
    target_interval = interval
    txt_out = ""
    for item in srt:
        start_time = timestamp_to_seconds(item.start)
        end_time = timestamp_to_seconds(item.end)
        item_text = item.text.strip()
        item_text = item_text.replace("\n", " ").strip()
        parsed_text = item_text.split(":", 1)
        if len(parsed_text) == 2:
            speaker = parsed_text[0].strip()
            transcription = parsed_text[1].strip()
            speaker = "\n<b>" + speaker + ":</b>"
            if end_time > target_interval - .2:  # Inject time stamp in [HH:MM:SS] format
                timecode = format_timecode(target_interval)
                target_interval += interval
                transcription = timecode + " " + transcription + " "
                print(timecode + " " + str(start_time) + "--" + str(end_time))
            txt_out += speaker + " " + transcription + " "
        else:
            transcription = item_text
            if end_time > target_interval - .2:  # Inject time stamp in [HH:MM:SS] format
                timecode = format_timecode(target_interval)
                target_interval += interval
                transcription = timecode + " " + transcription + " "
                print(timecode + " " + str(start_time) + "--" + str(end_time))
            txt_out += transcription + " "
    txt_out = txt_out.replace(' \n', '\n')
    f.write(txt_out.replace("  ", " ").strip())
    f.close()


def main():
    interval_seconds = 30  # Possible Values: 30, 60, 120, 180, 240, 300
    srt_path = os.path.join(os.getcwd(), "input-srt")
    txt_path = os.path.join(os.getcwd(), "output-txt")
    files = os.listdir(srt_path)
    count = 0
    for file in files:
        count += 1
        print(file + ", ", count)
        convert_srt_to_tsv(file, srt_path, txt_path, interval_seconds)


if __name__ == '__main__':
    main()
