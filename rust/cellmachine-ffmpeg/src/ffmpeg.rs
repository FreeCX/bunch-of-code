use std::io::Write;
use std::process::{ChildStdin, Command, Stdio};

pub struct Render(ChildStdin);

impl Render {
    pub fn create(output: &str, width: u32, height: u32, scale: u32, fps: u32) -> Render {
        #[rustfmt::skip]
        let arguments = [
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-video_size", &format!("{}x{}", width, height),
            "-r", &format!("{}", fps), "-i", "-", "-c:v", "libx264", "-preset", "slow", "-profile:v", "high",
            "-crf", "18", "-coder", "1", "-pix_fmt", "yuv420p", "-vf",
            &format!("scale=iw*{scale}:ih*{scale}"), "-sws_flags", "neighbor", "-sws_dither", "none",
            "-movflags", "+faststart", "-g", "30", "-bf", "2", "-y", &output,
        ];

        let mut process = match Command::new("ffmpeg").args(arguments).stdin(Stdio::piped()).spawn() {
            Err(why) => panic!("couldn't spawn ffmpeg: {}", why),
            Ok(process) => process,
        };
        let stdin = process.stdin.take().unwrap();

        Render(stdin)
    }

    pub fn append(&mut self, image: &[u8]) {
        if let Err(why) = self.0.write_all(image) {
            panic!("couldn't write to ffmpeg stdin: {}", why)
        };
    }
}
