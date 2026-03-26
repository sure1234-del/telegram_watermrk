import subprocess

def process_video(
    input_path,
    output_path,
    forced_text,
    user_text=None,
    position="bottom",
    speed=150,
    opacity=0.7,
    logo_path=None
):

    y_pos = {
        "top": "50",
        "middle": "h/2",
        "bottom": "h-60"
    }[position]

    watermark_text = forced_text
    if user_text:
        watermark_text += f" | {user_text}"

    drawtext = (
        f"drawtext=text='{watermark_text}':"
        f"x=w-mod(t*{speed}\\,w+tw):"
        f"y={y_pos}:"
        f"fontsize=35:"
        f"fontcolor=white@{opacity}"
    )

    if logo_path:
        filter_complex = (
            f"[0:v]{drawtext}[v1];"
            f"[v1][1:v]overlay=W-w-20:H-h-20"
        )

        command = [
            "ffmpeg",
            "-i", input_path,
            "-i", logo_path,
            "-filter_complex", filter_complex,
            "-codec:a", "copy",
            output_path
        ]
    else:
        command = [
            "ffmpeg",
            "-i", input_path,
            "-vf", drawtext,
            "-codec:a", "copy",
            output_path
        ]

    subprocess.run(command)