import sys
import logging

import beam_sequencer.pipeline


if __name__ == "__main__":
    logging.getLogger().setLevel(level=logging.INFO)
    beam_sequencer.pipeline.run(sys.argv)
