# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Default glyphmap writer. Writes rows like:


picosvg/regular/clipped/emoji_u270d_1f3fb.svg, "270d,1f3fb", g_270d_1f3fb

"""


from absl import app
from absl import flags
from nanoemoji.glyph import glyph_name
from nanoemoji.glyphmap import GlyphMapping
from nanoemoji import codepoints
from nanoemoji import features
from nanoemoji import util
from pathlib import Path
from typing import Sequence, Tuple

FLAGS = flags.FLAGS

flags.DEFINE_string("output_file", "-", "Output filename ('-' means stdout)")


def _glyphmappings(input_files: Sequence[str]) -> Tuple[GlyphMapping]:
    return tuple(
        GlyphMapping(Path(input_file), cps, glyph_name(cps))
        for input_file, cps in zip(
            input_files,
            tuple(codepoints.from_filename(Path(f).name) for f in input_files),
        )
    )


def main(argv):
    input_files = util.expand_ninja_response_files(argv[1:])
    with util.file_printer(FLAGS.output_file) as print:
        for gm in _glyphmappings(input_files):
            # filename, codepoint(s), glyph name
            print(gm.csv_line())


if __name__ == "__main__":
    app.run(main)
